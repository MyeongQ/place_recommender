const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

const User = require('../models/user');

module.exports = () => {
  passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_ID,
    clientSecret: process.env.GOOGLE_SECRET,
    callbackURL: '/auth/google/callback',
  }, async (accessToken, refreshToken, profile, done) => {
    console.log('Google profile', profile);
    /*
    try {
      const user = await User.findOrCreate({ 
        where: {
          email: profile.emails[0].value,
          nick: profile.displayName,
          snsId: profile.id,
          provider: profile.provider,
        }
      });
      done(null, user);
    } catch (error) {
      console.error(error);
      done(error);
    }
    */
    try {
      const exUser = await User.findOne({
        where: { snsId: profile.id, provider: 'google' },
      });
      if (exUser) {
        done(null, exUser);
      } else {
        const newUser = await User.create({
          email: profile.emails[0].value,
          nick: profile.displayName,
          snsId: profile.id,
          provider: 'google',
        });
        done(null, newUser);
      }
    } catch (error) {
      console.error(error);
      done(error);
    }
  }));
};