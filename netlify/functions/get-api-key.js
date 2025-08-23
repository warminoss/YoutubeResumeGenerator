exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // REMPLACEZ par votre vraie clé Gemini
  const API_KEY = 'AIzaSyCccIgov-nc_OiFQ0eXm4xnJpaWJ1rYsvE'; // ← Votre clé complète ici

  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      apiKey: API_KEY,
      message: 'Clé par défaut du propriétaire'
    })
  };
};
