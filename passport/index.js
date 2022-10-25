const passport = require('passport');
const local = require('./localStrategy');
const kakao = require('./kakaoStrategy');
const google = require('./googleStrategy');
const User = require('../models/user');
const { Review, Place } = require('../models');

module.exports = () => {
  passport.serializeUser((user, done) => {
    done(null, user.id); // 세션에 user의 id만 저장 > 메모리 효율
  });

  // { id: 3, 'connect.sid': s%321937626312 }

  passport.deserializeUser((id, done) => {
    User.findOne({ 
        where: { id },
        // req.user에 함께 저장할 데이터, 사용자 정보 불러올 때 항상 갖고옴
        include: [{
            model: Place,
            attributes: ['id', 'name'],
            as: 'Wish',
        }/*, {
            model: Review,
            attributes: ['id', 'content', 'rating'],
            as: 'Review',
        }*/],
    })  // id로 user를 찾아 req.user로 접근 가능하게 만듦
      .then(user => done(null, user)) // req.user, req.isAuthenticated()
      .catch(err => done(err));
  });

  local();
  kakao();
  google();
};