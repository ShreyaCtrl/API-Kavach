import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ApiItem from './ApiItem';

function ApiList() {
    const [apis, setApis] = useState([]);

    useEffect(() => {
        const fetchApis = async () => {
            try {
                const response = await axios.get('http://localhost:5000/list-apis', {
                    headers: {
                        'Authorization': `${localStorage.getItem('token')}` // Adjust the token retrieval method as needed
                    }
                });
                setApis(response.data.apis);
            } catch (error) {
                console.error('Error fetching APIs:', error);
            }
        };

        fetchApis();
    }, []);

    return (
        <div>
            <h2>API List</h2>
            <ul>
                {apis.map(api => (
                    <ApiItem key={api.id} api={api} />
                ))}
            </ul>
        </div>
    );
}

export default ApiList;
