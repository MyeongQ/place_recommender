const Sequelize = require('sequelize');

module.exports = class Like extends Sequelize.Model {
    static init(sequelize) {
        return super.init({
            PlaceId: {
                type: Sequelize.INTEGER,
                allowNull: false,
            },
            UserID: {
                type: Sequelize.INTEGER,
                allowNull: true,
            },
        }, {
            sequelize,
            timestamps: true,
            underscored: false,
            modelName: 'Like',
            tableName: 'likelist',
            paranoid: false, // 게시물 삭제시 진짜 삭제할 예정
            charset: 'utf8mb4',
            collate: 'utf8mb4_general_ci',
        });
    }

    static associate(db) {
        db.Like.belongsTo(db.User);
        db.Like.belongsTo(db.Review);
    }
};