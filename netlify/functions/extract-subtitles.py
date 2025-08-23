<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Subtitle Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1e40af;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        h1 {
            text-align: center;
            color: #1e40af;
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: bold;
        }

        .input-section {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1e40af;
        }

        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #fbbf24;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #1e40af;
            box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
        }

        .btn {
            background: #fbbf24;
            color: #1e40af;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
        }

        .btn:hover {
            background: #f59e0b;
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
            font-weight: 500;
        }

        .status.loading {
            background: #dbeafe;
            color: #1e40af;
            border-left: 4px solid #3b82f6;
        }

        .status.error {
            background: #fef2f2;
            color: #dc2626;
            border-left: 4px solid #ef4444;
        }

        .status.success {
            background: #f0fdf4;
            color: #16a34a;
            border-left: 4px solid #22c55e;
        }

        .result-section {
            margin-top: 30px;
            display: none;
        }

        .result-section h3 {
            color: #1e40af;
            margin-bottom: 15px;
            font-size: 1.5em;
        }

        .result-content {
            background: #fffbeb;
            border: 2px solid #fbbf24;
            border-radius: 8px;
            padding: 20px;
            margin-top: 15px;
            white-space: pre-wrap;
            line-height: 1.6;
            max-height: 400px;
            overflow-y: auto;
            color: #1e293b;
        }

        .download-btn {
            background: #1e40af;
            color: white;
            margin-top: 15px;
        }

        .download-btn:hover {
            background: #1e3a8a;
        }

        .api-key-section {
            background: #fffbeb;
            border: 2px solid #fbbf24;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }

        .note {
            font-size: 14px;
            color: #92400e;
            margin-top: 10px;
            font-style: italic;
        }

        .note a {
            color: #1e40af;
            text-decoration: none;
        }

        .note a:hover {
            text-decoration: underline;
        }

        .debug-info {
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            font-family: monospace;
            font-size: 12px;
            max-height: 200px;
            overflow-y: auto;
            display: none;
        }

        .debug-info.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 YouTube Subtitle Analyzer</h1>
        
        <div class="api-key-section">
            <label for="apiKey">🔑 Clé API Gemini :</label>
            <input type="password" id="apiKey" placeholder="Entrez votre clé API Gemini..." />
            <div class="note">
                Obtenez votre clé API gratuite sur <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a>
            </div>
        </div>

        <div class="input-section">
            <label for="youtubeUrl">🎥 URL YouTube :</label>
            <input type="text" id="youtubeUrl" placeholder="https://www.youtube.com/watch?v=..." />
        </div>

        <div class="input-section">
            <label for="subtitles">📝 Sous-titres (optionnel - copiez depuis YouTube) :</label>
            <textarea id="subtitles" rows="8" placeholder="Collez ici les sous-titres de la vidéo...

💡 Comment obtenir les sous-titres :
1. Allez sur YouTube
2. Cliquez sur 'CC' ou '⚙️' → Sous-titres
3. Cliquez sur 'Ouvrir la transcription'
4. Copiez tout le texte et collez ici"></textarea>
        </div>

        <button class="btn" onclick="processVideo()">
            ✨ Analyser la vidéo
        </button>

        <div id="status"></div>
        
        <div class="debug-info" id="debugInfo"></div>

        <div class="result-section" id="resultSection">
            <h3>📋 Résumé et analyse :</h3>
            <div class="result-content" id="resultContent"></div>
            <button class="btn download-btn" onclick="downloadResult()">
                📥 Télécharger le résumé (TXT)
            </button>
        </div>
    </div>

    <script>
        let analysisResult = '';
        let debugLogs = [];

        function log(message) {
            debugLogs.push(`[${new Date().toLocaleTimeString()}] ${message}`);
            document.getElementById('debugInfo').textContent = debugLogs.join('\n');
            document.getElementById('debugInfo').classList.add('show');
            console.log(message);
        }

        function showStatus(message, type = 'loading') {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
        }

        function hideStatus() {
            document.getElementById('status').innerHTML = '';
        }

        function extractVideoId(url) {
            const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/;
            const match = url.match(regex);
            return match ? match[1] : null;
        }

        async function extractSubtitlesWithAPI(videoId) {
            log(`Tentative extraction pour vidéo: ${videoId}`);
            
            // API 1: Transcript API directe
            try {
                log('Test API 1: YouTube Transcript API');
                const response = await fetch(`https://cors-anywhere.herokuapp.com/https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}&key=AIzaSyB-riBkMr8PZVVPqOXw3Kd_4E8Qa8BjLj8`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    log('API 1 réponse: ' + JSON.stringify(data).substring(0, 100));
                }
            } catch (e) {
                log('API 1 échouée: ' + e.message);
            }

            // API 2: Service externe
            try {
                log('Test API 2: Service externe');
                const response = await fetch(`https://api.freeapi.app/api/v1/public/youtube/transcript/${videoId}`);
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.data && data.data.transcript) {
                        log('✅ API 2 succès !');
                        return data.data.transcript;
                    }
                }
                log('API 2: Pas de données transcript');
            } catch (e) {
                log('API 2 échouée: ' + e.message);
            }

            // API 3: Alternative simple
            try {
                log('Test API 3: Alternative');
                const response = await fetch(`https://subtitles-for-youtube.p.rapidapi.com/subtitles/${videoId}.json`, {
                    headers: {
                        'X-RapidAPI-Key': 'demo', // Clé de démo
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    log('API 3 réponse: ' + JSON.stringify(data).substring(0, 100));
                }
            } catch (e) {
                log('API 3 échouée: ' + e.message);
            }

            // API 4: YouTube Data API v3 (sans clé)
            try {
                log('Test API 4: YouTube Data');
                const response = await fetch(`https://www.youtube.com/api/timedtext?v=${videoId}&lang=en&fmt=json3`);
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.events) {
                        const transcript = data.events
                            .filter(event => event.segs)
                            .map(event => event.segs.map(seg => seg.utf8).join(''))
                            .join(' ');
                        
                        if (transcript.length > 50) {
                            log('✅ API 4 succès ! Sous-titres trouvés');
                            return transcript;
                        }
                    }
                }
                log('API 4: Pas de sous-titres disponibles');
            } catch (e) {
                log('API 4 échouée: ' + e.message);
            }

            log('❌ TOUTES LES API ONT ÉCHOUÉ');
            throw new Error('Impossible d\'extraire les sous-titres. La vidéo n\'a peut-être pas de sous-titres auto-générés.');
        }

        async function extractSubtitles(videoUrl) {
            showStatus('🔍 Recherche des sous-titres...');
            
            const videoId = extractVideoId(videoUrl);
            if (!videoId) {
                throw new Error('ID vidéo introuvable dans l\'URL');
            }

            log(`=== DÉBUT EXTRACTION ===`);
            log(`URL: ${videoUrl}`);
            log(`Video ID: ${videoId}`);

            try {
                // Tentative d'extraction avec APIs publiques
                const subtitles = await extractSubtitlesWithAPI(videoId);
                log(`✅ Sous-titres extraits: ${subtitles.length} caractères`);
                return subtitles;
                
            } catch (error) {
                log(`❌ Extraction échouée: ${error.message}`);
                
                // Dernier recours: Indiquer à l'utilisateur quoi faire
                showStatus('❌ Extraction impossible. Voir les logs ci-dessous.', 'error');
                
                throw new Error(`Impossible d'extraire les sous-titres automatiquement.

SOLUTIONS:
1. Utilisez une vidéo avec sous-titres auto-générés activés
2. Ou créez un serveur local avec yt-dlp
3. Ou utilisez l'extension Chrome "YouTube Transcript"

VIDÉO TESTÉE: ${videoId}
TOUTES LES API ONT ÉCHOUÉ - Voir logs pour détails`);
            }
        }

        async function analyzeWithGemini(subtitles, apiKey, videoUrl) {
            showStatus('🤖 Analyse avec Gemini...');
            
            const videoId = extractVideoId(videoUrl);
            
            const prompt = `Analyse ces VRAIS sous-titres de la vidéo YouTube ${videoId} et crée un résumé détaillé en français :

**ANALYSE DEMANDÉE:**

1. **RÉSUMÉ GÉNÉRAL** (2-3 paragraphes)
2. **POINTS CLÉS PRINCIPAUX** (liste)
3. **DÉTAILS TECHNIQUES** mentionnés
4. **ANECDOTES/EXEMPLES** donnés
5. **CONCLUSION ET TAKEAWAYS**

**SOUS-TITRES À ANALYSER:**
${subtitles}

Crée une analyse SPÉCIFIQUE à ce contenu réel. Ne donne pas de réponse générique.`;

            try {
                const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-goog-api-key': apiKey
                    },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: prompt
                            }]
                        }],
                        generationConfig: {
                            temperature: 0.7,
                            topK: 40,
                            topP: 0.95,
                            maxOutputTokens: 2048
                        }
                    })
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Erreur API Gemini: ${response.status} - ${errorText}`);
                }

                const data = await response.json();
                
                if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                    return data.candidates[0].content.parts[0].text;
                } else {
                    throw new Error('Réponse invalide de Gemini');
                }
            } catch (error) {
                throw new Error(`Erreur analyse Gemini: ${error.message}`);
            }
        }

        async function processVideo() {
            const apiKey = document.getElementById('apiKey').value.trim();
            const videoUrl = document.getElementById('youtubeUrl').value.trim();
            const manualSubtitles = document.getElementById('subtitles').value.trim();

            // Reset des logs
            debugLogs = [];
            document.getElementById('debugInfo').classList.remove('show');

            if (!apiKey) {
                showStatus('❌ Clé API Gemini requise', 'error');
                return;
            }

            if (!videoUrl) {
                showStatus('❌ URL YouTube requise', 'error');
                return;
            }

            const videoId = extractVideoId(videoUrl);
            if (!videoId) {
                showStatus('❌ URL YouTube invalide', 'error');
                return;
            }

            const analyzeBtn = document.querySelector('.btn');
            analyzeBtn.disabled = true;

            try {
                let subtitles;

                // Priorité aux sous-titres manuels si fournis
                if (manualSubtitles && manualSubtitles.length > 50) {
                    log('✅ Utilisation des sous-titres manuels fournis');
                    subtitles = manualSubtitles;
                    analyzeBtn.textContent = 'Analyse en cours...';
                } else {
                    log('Aucun sous-titre manuel, tentative extraction automatique...');
                    analyzeBtn.textContent = 'Extraction en cours...';
                    subtitles = await extractSubtitles(videoUrl);
                    analyzeBtn.textContent = 'Analyse en cours...';
                }
                
                if (!subtitles || subtitles.trim().length < 20) {
                    throw new Error('Sous-titres trop courts (moins de 20 caractères)');
                }

                log(`Analyse de ${subtitles.length} caractères de sous-titres`);
                
                // Analyse avec Gemini
                analysisResult = await analyzeWithGemini(subtitles, apiKey, videoUrl);
                
                // Affichage
                document.getElementById('resultContent').textContent = analysisResult;
                document.getElementById('resultSection').style.display = 'block';
                
                showStatus('✅ Analyse terminée !', 'success');
                log(`✅ SUCCÈS - Analyse terminée pour ${videoId}`);
                
            } catch (error) {
                showStatus(`❌ ${error.message}`, 'error');
                log(`❌ ERREUR: ${error.message}`);
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = 'Analyser la vidéo';
            }
        }

        function downloadResult() {
            if (!analysisResult) {
                showStatus('❌ Aucun résultat à télécharger', 'error');
                return;
            }

            const videoUrl = document.getElementById('youtubeUrl').value;
            const videoId = extractVideoId(videoUrl);
            const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
            
            const filename = `youtube_analysis_${videoId}_${timestamp}.txt`;
            
            const content = `ANALYSE YOUTUBE - ${new Date().toLocaleString('fr-FR')}
============================================
URL: ${videoUrl}
ID Vidéo: ${videoId}
============================================

${analysisResult}

============================================
Logs d'extraction:
${debugLogs.join('\n')}
============================================`;

            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            showStatus('📥 Fichier téléchargé !', 'success');
            setTimeout(hideStatus, 3000);
        }

        // Test automatique au chargement
        window.addEventListener('load', function() {
            log('Application chargée');
            log('Prêt pour test d\'extraction');
            
            // Test avec une vidéo connue pour avoir des sous-titres
            setTimeout(() => {
                log('Pour tester: utilisez une vidéo populaire avec sous-titres auto-générés');
                log('Exemple: https://www.youtube.com/watch?v=dQw4w9WgXcQ');
            }, 1000);
        });

        // Test de la clé API
        document.getElementById('apiKey').addEventListener('blur', async function() {
            const apiKey = this.value.trim();
            if (apiKey && apiKey.length > 20) {
                try {
                    showStatus('Test clé API...', 'loading');
                    
                    const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-goog-api-key': apiKey
                        },
                        body: JSON.stringify({
                            contents: [{
                                parts: [{ text: "Test" }]
                            }]
                        })
                    });

                    if (response.ok) {
                        showStatus('✅ Clé API valide', 'success');
                        log('✅ Clé API Gemini validée');
                    } else {
                        showStatus('❌ Clé API invalide', 'error');
                        log('❌ Clé API Gemini invalide');
                    }
                } catch (error) {
                    showStatus('❌ Erreur test API', 'error');
                    log('❌ Erreur test API: ' + error.message);
                }
                
                setTimeout(hideStatus, 2000);
            }
        });
    </script>
</body>
</html>
