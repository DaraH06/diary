from flask import Flask,render_template,jsonify,request
from pymongo import MongoClient
from datetime import datetime

conn_string = 'mongodb+srv://test:test@cluster00.aw629as.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(conn_string)
db = client.DbNextGen

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/diary',methods=['GET'])
def getdiary():
    diary_packet = list(db.diary.find({},{'_id':False}))
    return jsonify({'diaries':diary_packet})

@app.route('/diary',methods=['POST'])
def postdiary():
    #sample_receive = request.form.get('sample_give')
    #print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    file_receive = request.files['file_give']
    extension = file_receive.filename.split('.')[-1]
    today = datetime.now()
    unique_id = today.strftime('%A-%d-%b-%Y-%H-%M-%S')
    file_name_image = f'static/img_title/upload-{unique_id}.{extension}'
    file_receive.save(file_name_image)

    profile_receive = request.files['profile']
    extension = file_receive.filename.split('.')[-1]
    today = datetime.now()
    unique_id = today.strftime('%A-%d-%b-%Y-%H-%M-%S')
    file_name_profile = f'static/profile/upload-{unique_id}.{extension}'
    profile_receive.save(file_name_profile)

    

    time = today.strftime ('%Y.%m.%d')
    #yang diminta om mentor korea :v
    # Jika title dan deskripsi tidak ada maka return error, image hanyalah opsional
    if not title_receive or not content_receive :
        return jsonify({'msg':'error data was incorrect'})
    else :
        # --- Save deskripsi dan judul ---
        doc = {
            'file' : file_name_image,
            'profile' : file_name_profile,
            'title' : title_receive,
            'content' : content_receive,
            'time' : time
        }
        # --- Kirim ke MongoDB
        db.diary.insert_one(doc)
        return jsonify({'msg':'data saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)