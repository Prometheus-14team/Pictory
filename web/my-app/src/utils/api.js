// api.js
export const fetchEvents = async () => {
    try {
      const response = await fetch('your-api-endpoint'); // 확인
      const data = await response.json();
      
      if (Array.isArray(data)) {
        return data;
      } else {
        throw new Error('Data is not an array');
      }
    } catch (error) {
      console.error('Error fetching events:', error);
      return []; // 실패시 빈 배열 반환
    }
  };
  