const express = require('express');
const passport = require('passport');
const bcrypt = require('bcrypt');
const {isLoggedIn, isNotLoggedIn } = require('./middlewares');
const User = require('../models/user');


const router = express.Router();

router.post('/join', isNotLoggedIn, async (req, res, next) => {
    const { email, nick, password } = req.body;
    try {
        const exUser = await User.findOne({ where: { email } });
        if (exUser) {  // 이미 가입한 이메일일 경우
            return res.redirect('/join?error=exist');
        }
        const hash = await bcrypt.hash(password, 12);
        await User.create({
            email,
            nick,
            password: hash,
        });
        return res.redirect('/map');
    } catch (error) {
        console.error(error);
        return next(error);
    }
});

router.post('/login', isNotLoggedIn, (req, res, next) => {
    passport.authenticate('local', (authError, user, info) => {
        if (authError) {
            console.error(authError);
            return next(authError);
        }
        if (!user) {
            return res.redirect(`/?loginError=${info.message}`);
        }
        return req.login(user, (loginError) => {
            if (loginError) {
                console.error(loginError);
                return next(loginError);
            }
            // 세션 쿠키를 브라우저로 전달 = 로그인 상태
            return res.redirect('/map');
        });
    }) (req, res, next);
});

router.get('/logout', isLoggedIn, (req, res) => {
    req.logout(() => { // 세션 쿠키를 지움
        req.session.destroy();  // 세션을 파괴
        res.redirect('/');  // 홈으로 이동
    });  
    
});

router.get('/kakao', passport.authenticate('kakao'));

router.get('/kakao/callback', passport.authenticate('kakao', {
    failureRedirect: '/',
}), (req, res) => {
    res.redirect('/');
});

router.get('/google', passport.authenticate('google', {
    scope: ['email', 'profile'],
}));

router.get('/google/callback', passport.authenticate('google', {
    failureRedirect: '/'
}), (req, res) => {
    res.redirect('/');
});

module.exports = router;