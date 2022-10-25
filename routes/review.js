const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const axios = require('axios');

const { Review, Hashtag, Place, User } = require('../models');
const { isLoggedIn } = require('./middlewares');

const router = express.Router();

// uploads 폴더가 없으면 만들어줌
/*try {
    fs.readdirSync('uploads');
} catch (error) {
    console.error('uploads 폴더가 없어 uploads 폴더를 생성합니다.');
    fs.mkdirSync('uploads');
}
*/
/*
const upload = multer({
    storage: multer.diskStorage({
        destination(req, file, cb) {
            cb(null, 'uploads/');
        },
        filename(req, file, cb) {
            const ext = path.extname(file.originalname);
            cb(null, path.basename(file.originalname, ext) + Date.now() + ext);
        },
    }),
    limits: { fileSize: 5 * 1024 * 1024 }, // 파일 용량 제한
});
*/

router.get('/:placeId', isLoggedIn, async (req, res, next) => {
    
    try{
        const reviews = await Review.findAll({
            where: {
                PlaceId: req.params.placeId,
            },
            include: [{
                model: User,
                attributes: ['nick'],
            }],
            limit: 100,
        })
        if(reviews) {
            console.log(reviews)
            res.json(reviews);
        } else {
            console.log(`cannot find reivews of Place ID: ${placeId}` )
            next(error);
        }
        
    } catch(error) {
        console.log(error);
        next(error);
    }
})

router.post('/:placeId', isLoggedIn, async(req, res, next) => {
    const { rating, content } = req.body;
    try{
        await Review.create({
            content,
            rating,
            UserId: req.user.id,
            PlaceId: req.params.placeId,
        });
        await axios.get("http://127.0.0.1:5000/makecsv");
        return res.redirect(`/review/${req.params.placeId}`);
    }catch (error) {
        console.error(error);
        return next(error);
    }
})

/*
router.post('/img', isLoggedIn, upload.single('img'), (req, res) => {
    console.log(req.file);
    // 실제 주소는 uploads, 요청 주소는 img
    // url을 front로 돌려보내 다음 게시물 작성시 이미지 경로와 함께 전송 가능
    res.json({ url: `/img/${req.file.filename}`});
});

const upload2 = multer();
// 업로드할 이미지가 없으므로 upload.none
router.post('/', isLoggedIn, upload2.none(), async(req, res, next) => {
    try {
        const review = await Review.create({
            content: req.body.content,
            img: req.body.url,
            UserId: req.user.id,
        });
        const hashtags = req.body.content.match(/#[^\s#]+/g);  // 정규 표현식으로 hashtag 추출
        if (hashtags) {
            const result = await Promise.all( //?
                hashtags.map(tag => {
                    return Hashtag.findOrCreate({  // [[있는거, false], [없는거, true]]
                        where: { title: tag.slice(1).toLowerCase() },
                    })
                }),
            );
            await review.addHashtags(result.map(r => r[0]));
        }
        res.redirect('/');
    } catch (err) {
        console.error(err);
        next(err);
    }
});

router.delete('/:reviewId', isLoggedIn, async (req, res, next) => {
    try{
        const myId = req.user.id;
        const review = await Review.findOne({ where: { id: req.params.postId } });
        console.log(review);
        if (myId === review.UserId ) {
            await Review.destroy({ where: { id: review.id } });
            res.send('success');
        } else {
            res.status(404).send('게시물 삭제 실패');
        }
    } catch (error) {
        console.error(error);
        next(error);
    }
})
*/
module.exports = router;