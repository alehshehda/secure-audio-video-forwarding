import { useState, useEffect } from "react";
import api from "../api";

function Home() {
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);

    const getFiles = () => {
        api
            .get('/api/video/list/')
            .then((res) => res.data)
            .then((data) => { setFiles(data); console.log(data); })
            .catch((error) => alert(error));
    };

    const uploadFiles = () => {
        if (!selectedFile)
            return alert('Please select a file');

        setUploading(true);
        const formData = new FormData();
        formData.append('file', selectedFile);

        api
            .post('/api/video/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            .then((res) => {
                if (res.status === 201) {
                    alert('File uploaded successfully');
                    getFiles();
                } else {
                    alert('File upload failed');
                }
            })
            .catch((err) => alert(err))
            .finally(() => setUploading(false));
    }

    useEffect(() => {
        getFiles();
    }, []);

    const deleteFile = (id) => {
        api
            .delete(`/api/video/delete/${id}/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            .then((res) => {
                if (res.status === 204) {
                    alert('File deleted successfully');
                    getFiles();
                } else {
                    alert('File deletion failed');
                }
            })
            .catch((err) => alert(err));
    }

    const downloadFile = (file) => {
        api
            .get(`/api/video/download/${file.id}/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                responseType: 'blob'
            })
            .then((res) => {
                if (res.status === 200) {
                    const url = window.URL.createObjectURL(new Blob([res.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', file.file.split('/').pop()); // Устанавливаем имя файла
                    document.body.appendChild(link);
                    link.click();
                    link.parentNode.removeChild(link);
                    alert('File downloaded successfully');
                } else {
                    alert('File download failed');
                }
            })
            .catch((err) => alert(err));
    }

    return (
        <div>
            <h1>Home</h1>
            {uploading && <p>Loading...</p>}
            {error && <p>Error: {error.message}</p>}
            <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
            <button onClick={uploadFiles}>Upload File</button>
            <ul>
                {files.map((file) => (
                    <li key={file.id}>
                        {file.file}
                        <button onClick={() => downloadFile(file)}>Download</button>
                        <button onClick={() => deleteFile(file.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Home;