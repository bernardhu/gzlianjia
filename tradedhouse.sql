DROP TABLE IF EXISTS "tradedhouse";
CREATE TABLE "tradedhouse" (
    "id" INTEGER NOT NULL PRIMARY KEY, 
    "xiaoqu" VARCHAR(255) NOT NULL, 
    "houseType" VARCHAR(255) NOT NULL, 
    "square" VARCHAR(255) NOT NULL, 
    "houseUrl" VARCHAR(255) NOT NULL, 
    "orientation" VARCHAR(255) NOT NULL, 
    "decoration" VARCHAR(255) NOT NULL, 
    "elevator" VARCHAR(255) NOT NULL, 
    "floor" VARCHAR(255) NOT NULL, 
    "build" VARCHAR(255) NOT NULL, 
    "price" VARCHAR(255) NOT NULL, 
    "tradeDate" DATETIME NOT NULL, 
    "bid" VARCHAR(255) NOT NULL, 
    "cycle" VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS "districhouse";
CREATE TABLE "districhouse" (
    "id" INTEGER NOT NULL PRIMARY KEY, 
    "district" VARCHAR(255) NOT NULL, 
    "bizcircle" VARCHAR(255) NOT NULL, 
    "history" VARCHAR(255) NOT NULL, 
    "ref" VARCHAR(255) NOT NULL, 
    "avgpx" VARCHAR(255) NOT NULL, 
    "onsell" VARCHAR(255) NOT NULL 
);
