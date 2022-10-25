const express = require('express');
const path = require('path');
const { isLoggedIn, isNotLoggedIn } = require('./middlewares');
const { User, Review, Hashtag, Like, Wish, Place } = require('../models');
const bcrypt = require('bcrypt');
const { Op } = require('sequelize');
const axios = require("axios");

const router = express.Router();

router.use((req, res, next) => {
    res.locals.user = req.user; // 모든 라우터에서 req.user가 쓰일 수 있으므로 위에 선언
    res.locals.followerCount =  0;
    res.locals.followingCount =  0;
    res.locals.followerIdList = [];
    res.locals.likeList = [];
    next();
});

router.get('/map', isLoggedIn, (req, res) => {
    res.sendFile(path.join(__dirname, 'my-app/build/index.html'))
})

router.get('/search/:term', isLoggedIn, async (req, res, next) => {
    const term = req.params.term;
    try{
        const places = await Place.findAll(
            {where: {
                [Op.or]: [
                    { name: {[Op.like]: `%${term}%`} }, 
                    { detail: {[Op.like]: `%${term}%`} }, 
                    { location: {[Op.like]: `%${term}%`} }, 
                    { keywords: {[Op.like]: `%${term}%`} },
                ]
            },
            limit: 20,
        });
        //console.log(term);
        res.json(places);
    }catch (error) {
        console.error(error);
        next(error);
    }
})

router.get('/recommend', isLoggedIn, async (req, res, next) => {
    
    try{
        const user = await User.findOne({where: {id:req.user.id}});
        console.log(req.user.id, user.id)
        
        const reviews = await user.getReviews();
        console.log(reviews);
        if (reviews){
            if (reviews.length < 5){
                const places = await Place.findAll({
                    order: [['numReviews', 'DESC'], ['avgRating', 'DESC']],
                    limit: 10,
                });
                res.json(places);    
            }
            else {
                // flask 서버로 추천 요청
                const test_userId = 1
                const placeIds = reviews.map(x => x.PlaceId)
                console.log(placeIds)
                const test_reviews = []
                try{
                    var response = await axios.get(`http://127.0.0.1:5000/lfcf?userId=${test_userId}&visited=${placeIds}`)
                    console.log(response.data)
                    const result = response.data.result.map(x => x[0]);
                    console.log(result);
                    
                    const places = await Place.findAll({
                        where: { id: {[Op.in]: result }},
                    })
                    res.json(places);
                    
                }
                catch (error) {
                    console.log(error, "flask error");
                }
                
                //const places=[]
                console.log("req to flask");
                //res.json(places);    
            }
        } else{
            const places = await Place.findAll({
                order: [['numReviews', 'DESC'], ['avgRating', 'DESC']],
                limit: 10,
            });
            res.json(places);
        }
        // reviews가 0개라면 /popular로 요청
        // reveiws가 5개 미만이라면 flask server로 요청
        // reveiws가 5개 이상이라면 flask server로 요청
        //console.log(term);
    }catch (error) {
        console.error(error);
        next(error);
    }
})

router.get('/login', isNotLoggedIn, (req, res) => {
    console.log('start');
    res.render('login', { title: '로그인'});
})

router.get('/profile', isLoggedIn, (req, res) => {
    res.render('profile', { title: '내 정보 - NodeBird' });
});

router.get('/join', isNotLoggedIn, (req, res) => {
    res.render('signup', { title: '회원 가입'});
});

router.get('/update', isLoggedIn, (req, res) => {
    res.render('update', { title: '정보 수정 - NodeBird' });
});

// put???
router.post('/update', isLoggedIn, async (req, res, next) => {
    try {
        const { nick, password } = req.body;
        const hash = await bcrypt.hash(password, 12);
        await User.update(
            { 
                nick,
                password: hash,
            }, 
            { where: { id: req.user.id } }
        )
        console.log('정보 수정 완료');
        return res.redirect('/');
    } catch (error) {
        console.error(error);
        next(error);
    }
});

router.get('/', async (req, res, next) => {
    try {
        const reviews = await Review.findAll({
            include: {
                model: User,
                attributes: ['id', 'nick'],
            },
            order: [['createdAt', 'DESC']],
        });
        console.log(reviews);
        res.render('login', {
            title: 'NodeBird',
            twits: reviews,
        });
    } catch (err) {
        console.error(err);
        next(err);
    }
    
});
// GET /hashtag?hashtag=노드
router.get('/hashtag', async(req, res, next) => {
    const query = req.query.hashtag;
    if (!query) {
        return res.redirect('/');
    }
    try {
        const hashtag = await Hashtag.findOne({ where: { title: query } });
        let reviews = [];
        if (hashtag) {
            reviews = await hashtag.getReviews({ include: [{ model: User, attribute: [ 'id', 'nick' ] }] });
        }

        return res.render('main', {
            title: `${query} | NodeBird`,
            twits: reviews,
        });
    } catch (error) {
        console.error(error);
        return next(error);
    }
});

module.exports = router;