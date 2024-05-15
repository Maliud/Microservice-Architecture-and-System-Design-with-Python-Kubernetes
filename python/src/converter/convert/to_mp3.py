import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # boş temp dosyası

    tf = tempfile.NamedTemporaryFile()

    # VİDEO İÇERİĞİ

    out = fs_videos.get(ObjectId(message["video_fid"]))

    #boş dosyaya video içeriği ekleyin

    tf.write(out.read())

    # geçici video dosyasından video oluşturma

    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # dosyaya ses yazma

    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    #dosyayı mongoya kayıt etme

    f = open(tf_path,"rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange= "",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "mesaj yayınlanamadı"
