DROP TABLE IF EXISTS "tradedhouse";
CREATE TABLE "tradedhouse" (
    "id" INTEGER NOT NULL PRIMARY KEY, 
    "xiaoqu" VARCHAR(255) NOT NULL, 
    "houseType" VARCHAR(64) NOT NULL, 
    "square" REAL NOT NULL, 
    "houseUrl" VARCHAR(255) NOT NULL, 
    "orientation" VARCHAR(32) NOT NULL, 
    "decoration" VARCHAR(32) NOT NULL, 
    "elevator" VARCHAR(32) NOT NULL, 
    "floorLevel" VARCHAR(32) NOT NULL, 
    "floorTotal" INTEGER NOT NULL, 
    "build" INTEGER NOT NULL, 
    "price" INTEGER NOT NULL, 
    "tradeDate" DATETIME NOT NULL, 
    "bid" INTEGER NOT NULL, 
    "deal" REAL NOT NULL, 
    "cycle" INTEGER NOT NULL,
    "district" VARCHAR(32) NOT NULL, 
    "bizcircle" VARCHAR(32) NOT NULL
);

CREATE TABLE "renthouse" (
    "id" INTEGER NOT NULL PRIMARY KEY, 
    "xiaoqu" VARCHAR(255) NOT NULL, 
    "houseType" VARCHAR(64) NOT NULL, 
    "square" REAL NOT NULL, 
    "houseUrl" VARCHAR(255) NOT NULL, 
    "orientation" VARCHAR(32) NOT NULL, 
    "elevator" VARCHAR(32) NOT NULL, 
    "floorLevel" VARCHAR(32) NOT NULL, 
    "floorTotal" INTEGER NOT NULL, 
    "build" INTEGER NOT NULL, 
    "avg" INTEGER NOT NULL, 
    "price" INTEGER NOT NULL, 
    "loan" INTEGER NOT NULL, 
    "loanRet" INTEGER NOT NULL, 
    "seen" INTEGER NOT NULL, 
    "district" VARCHAR(32) NOT NULL, 
    "bizcircle" VARCHAR(32) NOT NULL
);

CREATE TABLE "bidhouse" (
    "id" INTEGER NOT NULL PRIMARY KEY, 
    "xiaoqu" VARCHAR(255) NOT NULL, 
    "houseType" VARCHAR(64) NOT NULL, 
    "square" REAL NOT NULL, 
    "houseUrl" VARCHAR(255) NOT NULL, 
    "orientation" VARCHAR(32) NOT NULL, 
    "decoration" VARCHAR(32) NOT NULL, 
    "elevator" VARCHAR(32) NOT NULL, 
    "floorLevel" VARCHAR(32) NOT NULL, 
    "floorTotal" INTEGER NOT NULL, 
    "build" INTEGER NOT NULL, 
    "price" INTEGER NOT NULL, 
    "avg" INTEGER NOT NULL, 
    "bid" REAL NOT NULL, 
    "watch" INTEGER NOT NULL, 
    "release" INTEGER NOT NULL, 
    "seen" INTEGER NOT NULL, 
    "district" VARCHAR(32) NOT NULL, 
    "bizcircle" VARCHAR(32) NOT NULL
);

DROP TABLE IF EXISTS "districhouse";
CREATE TABLE "districhouse" (
    "id" INTEGER NOT NULL PRIMARY KEY, 
    "name" VARCHAR(255) NOT NULL, 
    "district" VARCHAR(32) NOT NULL, 
    "bizcircle" VARCHAR(32) NOT NULL, 
    "historyRange" INTEGER NOT NULL, 
    "historySell" INTEGER NOT NULL, 
    "ref" VARCHAR(255) NOT NULL, 
    "avgpx" INTEGER NOT NULL, 
    "onsell" INTEGER NOT NULL 
);
