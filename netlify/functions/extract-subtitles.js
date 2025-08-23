const ytDlp = require('yt-dlp-wrap').default;
const fs = require('fs').promises;
const path = require('path');
const { tmpdir } = require('os');

exports.handler = async (event, context) => {
  // Headers CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Gérer les requêtes OPTIONS (CORS preflight)
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Méthode non autorisée' })
    };
  }

  try {
    const { url } = JSON.parse(event.body);
    
    if (!url || (!url.includes('youtube.com') && !url.includes('youtu.be'))) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'URL YouTube invalide' })
      };
    }

    // Créer un dossier temporaire unique
    const tempDir = path.join(tmpdir(), `yt-${Date.now()}`);
    await fs.mkdir(tempDir, { recursive: true });

    try {
      // Configuration yt-dlp
      const ytDlpPath = await ytDlp.downloadFromGithub();
      const ytDlpWrap = new ytDlp(ytDlpPath);

      // Options pour extraire uniquement les sous-titres
      const options = [
        '--write-subs',
        '--write-auto-subs',
        '--skip-download',
        '--sub-langs', 'fr,en,fr-FR,en-US',
        '--sub-format', 'vtt',
        '--output', `${tempDir}/%(title)s.%(ext)s`,
        url
      ];

      // Exécuter yt-dlp
      await ytDlpWrap.exec(options);

      // Chercher les fichiers de sous-titres
      const files = await fs.readdir(tempDir);
      const subtitleFiles = files.filter(f => f.endsWith('.vtt'));

      if (subtitleFiles.length === 0) {
        throw new Error('Aucun sous-titre trouvé pour cette vidéo');
      }

      // Lire le premier fichier de sous-titres trouvé
      const subtitlePath = path.join(tempDir, subtitleFiles[0]);
      const subtitleContent = await fs.readFile(subtitlePath, 'utf8');

      // Parser le contenu VTT pour extraire le texte seul
      const textLines = subtitleContent
        .split('\n')
        .filter(line => {
          const trimmed = line.trim();
          return trimmed && 
                 !trimmed.startsWith('WEBVTT') && 
                 !trimmed.includes('-->') && 
                 !trimmed.match(/^\d+$/) &&
                 !trimmed.startsWith('NOTE');
        })
        .map(line => line.replace(/<[^>]*>/g, '').trim()) // Supprimer les tags HTML
        .filter(line => line.length > 0);

      const extractedText = textLines.join(' ');

      // Nettoyer le dossier temporaire
      await fs.rmdir(tempDir, { recursive: true });

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          subtitles: extractedText,
          language: subtitleFiles[0].includes('fr') ? 'fr' : 'auto',
          message: 'Sous-titres extraits avec succès'
        })
      };

    } catch (extractError) {
      // Nettoyer en cas d'erreur
      try {
        await fs.rmdir(tempDir, { recursive: true });
      } catch {}
      throw extractError;
    }

  } catch (error) {
    console.error('Erreur:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: `Erreur d'extraction: ${error.message}`,
        details: 'Vérifiez que la vidéo existe et a des sous-titres disponibles'
      })
    };
  }
};