const Sequelize = require('sequelize');

module.exports = class Review extends Sequelize.Model {
    static init(sequelize) {
        return super.init({
            content: {
                type: Sequelize.STRING(300),
                alowNull: true,
            },
            rating: {
                type: Sequelize.INTEGER(1) ,
                allowNull: false,
            },
            img: {
                type: Sequelize.STRING(200),
                allowNull: true,
            },
        }, {
            sequelize,
            timestamps: true,
            underscored: false,
            modelName: 'Review',
            tableName: 'reviews',
            paranoid: true,
            charset: 'utf8',
            collate: 'utf8_general_ci'
        });
    }

    static associate(db) {
        db.Review.belongsTo(db.User);
        db.Review.belongsTo(db.Place);
        db.Review.belongsToMany(db.User, {
            as: "Likes",
            through: "LikeList",
        })
    };
};