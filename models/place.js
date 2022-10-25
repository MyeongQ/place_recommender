const Sequelize = require('sequelize');

module.exports = class Place extends Sequelize.Model {
    static init(sequelize) {
        return super.init({
            name: {
                type: Sequelize.STRING(40),
                alowNull: false,
            },
            avgRating: {
                type: Sequelize.FLOAT(2) ,
                allowNull: true,
            },
            numReviews: {
                type: Sequelize.INTEGER(8),
                allowNull: false,
                defaultValue: 0,
            },
            detail: {
                type: Sequelize.STRING(100),
                allowNull: true,
            },
            type: {
                type: Sequelize.STRING(20),
                allowNull: true,
            },
            location: {
                type: Sequelize.STRING(50),
                allowNull: true,
            },
            latitude: {
                type: Sequelize.DECIMAL(9,6) ,
                allowNull: false,
            },
            longitude: {
                type: Sequelize.DECIMAL(9,6),
                allowNull: false,
            },
            keywords: {
                type: Sequelize.STRING(100),
                allowNull: true,
            },
            clustering: {
                type: Sequelize.INTEGER(3),
                allowNull: true,
            }
        }, {
            sequelize,
            timestamps: true,
            underscored: false,
            modelName: 'Place',
            tableName: 'places',
            paranoid: true,
            charset: 'utf8',
            collate: 'utf8_general_ci'
        });
    }
    static associate(db) {
        db.Place.hasMany(db.Review, { as: 'Reviews'});
        db.Place.belongsToMany(db.User, { as: 'Wish', through: 'WishList' });
        db.Place.belongsToMany(db.Hashtag, { through: 'PlaceHashtag' });
    };
}