const express = require('express');

const { isLoggedIn } = require('./middlewares');
const { User, Place } = require('../models');

const router = express.Router();

router.post('/:place_id', isLoggedIn, async (req, res, next ) => {
    try {
        const user = await User.findOne({ where: {  id: req.user.id } });
        if (user) {
            await user.addWish(parseInt(req.params.place_id, 10));
            res.send('success');
        } else {
            res.status(404).send('no user');
        }
    } catch (error) {
        console.error(error);
        next(error);
    };
});

router.delete('/:place_id', isLoggedIn, async (req, res, next) => {
    try {
        const user = await User.findOne({ where: {  id: req.user.id } });
        if (user) {
            await user.removeWish(parseInt(req.params.place_id, 10));
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