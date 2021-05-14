const express = require('express')
const formidable = require('formidable')
const mv = require('mv')
// const upload = multer({dest: __dirname + '/uploads/images'});
const  { spawn } = require('child_process')
// const { PythonShell } = require('python-shell')
const fs = require('fs')
var moduleLoaded = 1
var pred

const app = express()

let port = process.env.PORT;
if(port == null || port =="") {
  port = 3000;
}

app.use(express.urlencoded({extended: false}))
app.use(express.json())


app.use(express.static('public'));
app.set('views', 'views')
app.set('view engine', 'ejs')

app.get('/', (req, res) => {
    res.render('index')
    return res.end();
})

let data = {
    '0' : "Black Grass",
    '1' : "Charlock",
    '2' : "Cleavers",
    '3' : "Common Chickweed",
    '4' : "Common Wheat",
    '5' : "Fat Hen",
    '6' : "Losse Silky Bent",
    '7' : "Maize",
    '8' : "Scentless Mayweed",
    '9' : "Shepherds Purse",
    '10' : "Small-flowered Cranesbill",
    '11' : "Sugar beet"
}

app.post('/fileupload', (req, res) => {
    let form = new formidable.IncomingForm()
    form.parse(req, (err, fields, files) => {
        let oldpath = files.filetoupload.path
        let newpath = "F:/VIT/SEM 6 (Win 20-21)/Software Engineering/Project/Web App/test.png"
        mv(oldpath, newpath, function (err) {
            if(err) throw err
            const python = spawn('python', ['./detect.py']);
            python.stdout.on('data', function (data) {
            result = data.toString()
            });
            python.on('close', (code) => {
            console.log(result);
            result = result.trim()
            console.log(result);
            mv("./test.png", "./public/test.png" , function (err){
                res.render('result', {species: data[result]})
            })
            
            });
        })
    })
})

app.listen(3000)