const express = require('express');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');
const path = require('path');
const session = require('express-session');
const nunjucks = require('nunjucks');
const dotenv = require('dotenv');
const passport = require('passport');

dotenv.config();
const pageRouter = require('./routes/page');
const authRouter = require('./routes/auth');
const reviewRouter = require('./routes/review');
const userRouter = require('./routes/user');
const likeRouter = require('./routes/like');
const wishRouter = require('./routes/wish');
const { sequelize } = require('./models');
const passportConfig = require('./passport');

const app = express();
passportConfig(); // 패스포트 설정
app.set('port', process.env.PORT || 8001);
app.set('view engine', 'html');
nunjucks.configure('views', {
    express: app,
    watch: true,
});
sequelize.sync({ force: false })
    .then(() => {
        console.log("DB 연결 성공");
    })
    .catch((err) => {
        console.error(err);
    });

app.use(morgan('dev'));
app.use('/map', express.static(path.join(__dirname, 'my-app/build')));
app.use('/', express.static(path.join(__dirname, 'views')));//my-app/build

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(session({
    resave: false,
    saveUninitialized: false,
    secret: process.env.COOKIE_SECRET,
    cookie:{
        httpOnly: true,
        secure: false,
    },
}));
app.use(passport.initialize());
app.use(passport.session());

app.use('/', pageRouter)
app.use('/auth', authRouter);
app.use('/review', reviewRouter);
app.use('/user', userRouter);
app.use('/like', likeRouter);
app.use('/wish', wishRouter);

app.use((req, res, next) => {
    const error = new Error(`${req.method} ${req.url} 라우터가 없습니다.`);
    error.status = 404;
    next(error);
});

app.use((err, req, res, next) => {
    res.locals.message = err.message;
    res.locals.error = process.env.NODE_ENV !== 'production' ? err: {};
    res.status(err.status || 500)
    res.render('error');
})

app.listen(app.get('port'), () => {
    console.log(app.get('port'), '번 포트에서 대기 중');
});

/*
    passport 공식문서: www.passportjs.org
    passport-local 공식문서: www.npmjs.com/package/passport-local
    passport-kakao 공식문서: www.npmjs.com/package/passport-kakao
    passport-google 공식문서: www.npmjs.com/package/passport-google-oauth20
    bcrypt 공식문서: www.npmjs.com/package/bcrypt
 */