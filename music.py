from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('music.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'default_search': 'ytsearch',
            'noplaylist': True,
            'geo_bypass': True,
            'postprocessors': [{  # Ensures we get a playable URL
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                video = result['entries'][0]
                return jsonify({
                    "title": video.get('title'),
                    "audio_url": video.get('url'),  # This is the actual playable URL
                    "thumbnail": video.get('thumbnail'),
                })
            else:
                return jsonify({"error": "No results found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
