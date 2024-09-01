// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { toast } from 'sonner';

// function ApiCountWidget() {
//     const [apiCount, setApiCount] = useState(0);
//     const token = localStorage.getItem('token'); // Retrieve the token from localStorage


//     // Function to fetch the number of APIs
//     const fetchApiCount = async () => {
//         try {
//             const response = await axios.post('http://localhost:5000/check-new-apis',{                
//                 headers: {
//                     'Authorization': `${token}`
//                 }})  // Adjust the URL as needed
//             const newApis = response.data.newApis || [];
//             const newApiCount = newApis.length + apiCount;

//             if (newApiCount > apiCount) {
//                 setApiCount(newApiCount);
//                 toast.success('New API detected! Total APIs: ' + newApiCount, {
//                     duration: 2000,
//                 });
//             }
//         } catch (error) {
//             toast.error('Error fetching API data: ' + error.message, {
//                 duration: 2000,
//             });
//         }
//     };

//     useEffect(() => {
//         // Fetch the API count initially
//         fetchApiCount();

//         // Set up an interval to check for new APIs periodically
//         const intervalId = setInterval(fetchApiCount, 10000); // Check every 10 seconds

//         // Clear the interval when the component unmounts
//         return () => clearInterval(intervalId);
//     }, [apiCount]);

//     return (
//         <div className="api-count-widget">
//             <h3>Total APIs: {apiCount}</h3>
//         </div>
//     );
// }

// export default ApiCountWidget;

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';

function ApiCountWidget() {
    const [apiCount, setApiCount] = useState(0);
    const token = localStorage.getItem('token'); // Retrieve the token from localStorage

    // Function to fetch the number of APIs
    const fetchApiCount = async () => {
        try {
            const response = await axios.get('http://localhost:5000/list-apis', {
                headers: {
                    'Authorization': `Bearer ${token}` // Ensure Bearer token is used
                }
            });

            const apis = response.data.apis || [];
            const newApiCount = apis.length;

            if (newApiCount !== apiCount) {
                setApiCount(newApiCount);
                toast.success(`API count updated! Total APIs: ${newApiCount}`, {
                    duration: 2000,
                });
            }
        } catch (error) {
            if (error.response && error.response.status === 403) {
                toast.error('Authorization failed. Please log in again.', {
                    duration: 2000,
                });
            } else {
                toast.error('Error fetching API data: ' + error.message, {
                    duration: 2000,
                });
            }
        }
    };

    useEffect(() => {
        // Fetch the API count initially
        fetchApiCount();

        // Set up an interval to check for new APIs periodically
        const intervalId = setInterval(fetchApiCount, 10000); // Check every 10 seconds

        // Clear the interval when the component unmounts
        return () => clearInterval(intervalId);
    }, [apiCount]);

    return (
        <div className="api-count-widget">
            <h3>Total APIs: {apiCount}</h3>
        </div>
    );
}

export default ApiCountWidget;
