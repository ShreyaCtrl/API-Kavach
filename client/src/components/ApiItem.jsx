import React from 'react';

function ApiItem({ api }) {
    const handleClick = () => {
        console.log('API Details:', api);
        // You can perform other actions here, like navigating to another page or fetching more details
    };

    return (
        <li onClick={handleClick} style={{ cursor: 'pointer', marginBottom: '10px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}>
            <h3>{api.name}</h3>
            <p><strong>Description:</strong> {api.description}</p>
            <p><strong>Created Date:</strong> {api.createdDate}</p>
            <p><strong>Version:</strong> {api.version}</p>
            <p><strong>Stages:</strong> {api.stages.join(', ')}</p>
        </li>
    );
}

export default ApiItem;
