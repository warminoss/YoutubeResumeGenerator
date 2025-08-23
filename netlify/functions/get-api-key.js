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

  // Votre clé API sécurisée dans le fichier
  const API_KEY = 'AIzaSyCccIgov-nc_OiFQ0eXm4xnJpaWJ1rYsvE';

  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      apiKey: API_KEY,
      owner: 'Configuré par le propriétaire',
      message: 'Clé API par défaut chargée'
    })
  };
};
