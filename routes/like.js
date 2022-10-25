const express = require('express');

const { isLoggedIn } = require('./middlewares');
const { User, Review } = require('../models');

const router = express.Router();

router.post('/:review_id', isLoggedIn, async (req, res, next ) => {
    try {
        const user = await User.findOne({ where: {  id: req.user.id } });
        if (user) {
            await user.addLike(parseInt(req.params.review_id, 10));
            res.send('success');
        } else {
            res.status(404).send('no user');
        }
    } catch (error) {
        console.error(error);
        next(error);
    };
});

router.delete('/:review_id', isLoggedIn, async (req, res, next) => {
    try {
        const user = await User.findOne({ where: {  id: req.user.id } });
        if (user) {
            await user.removeLike(parseInt(req.params.review_id, 10));
            res.send('success');
        } else {
            res.status(404).send('no user');
        }
    } catch (error) {
        console.error(error);
        next(error);
    };
})

module.exports = router;