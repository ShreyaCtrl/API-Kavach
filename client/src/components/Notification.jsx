import React from 'react'
import { toast} from 'sonner';

const Notification = ({message, type}) => {
    // const notify = () => {
    //     toast(message, {
    //       type: type,
    //       duration: 4000,
    //       position: 'top-right',
    //       style: {
    //         background: type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : type === 'warning' ? '#fff3cd' : '#d1ecf1',
    //         color: type === 'success' ? '#155724' : type === 'error' ? '#721c24' : type === 'warning' ? '#856404' : '#0c5460',
    //       },
    //     });
    //   };

    const showToast = () => {
      switch (type) {
        case 'success':
          toast.success(message);
          break;
        case 'error':
          toast.error(message);
          break;
        case 'info':
          toast.info(message);
          break;
        case 'warning':
          toast.warning(message);
          break;
        default:
          toast(message);
      }
    };


     React.useEffect(() => {
    if (message) {
      showToast();
    }
  }, [message, type]);

  return null;
  // return <Toaster position='top-right'/>;
}

export default Notification
