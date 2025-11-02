/**
 * Pokemon TCG Set Theme Lookup Table
 * Based on official Pokemon TCG set information
 * Maps set abbreviations to gradient color schemes
 * 
 * Format: {
 *   abbreviation: {
 *     name: "Official Set Name",
 *     colors: [color1, color2, color3],
 *     angle: 135,
 *     era: "Era Name",
 *     releaseDate: "YYYY-MM",
 *     route: "/sets/{abbreviation}" // Future routing
 *   }
 * }
 */

const POKEMON_TCG_SET_THEMES = {
    // ============================================
    // BASE SET ERA
    // ============================================
    'BS': {
        name: 'Base Set',
        colors: ['#CC0000', '#FFDE00', '#003DA5'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '1999-01',
        route: '/sets/bs'
    },
    'BS1': {
        name: 'Base Set',
        colors: ['#CC0000', '#FFDE00', '#003DA5'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '1999-01',
        route: '/sets/bs1'
    },
    'BS2': {
        name: 'Base Set 2',
        colors: ['#990000', '#FFDE00', '#002966'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '2000-02',
        route: '/sets/bs2'
    },
    'JNG': {
        name: 'Jungle',
        colors: ['#228B22', '#FFD700', '#8B4513'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '1999-06',
        route: '/sets/jng'
    },
    'FOS': {
        name: 'Fossil',
        colors: ['#708090', '#4682B4', '#2F4F4F'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '1999-10',
        route: '/sets/fos'
    },
    'TR': {
        name: 'Team Rocket',
        colors: ['#000000', '#8B0000', '#2F2F2F'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '2000-04',
        route: '/sets/tr'
    },
    'G1': {
        name: 'Gym Heroes',
        colors: ['#FF4500', '#FFD700', '#FF6347'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '2000-08',
        route: '/sets/g1'
    },
    'G2': {
        name: 'Gym Challenge',
        colors: ['#1E90FF', '#FFD700', '#FF1493'],
        angle: 135,
        era: 'Base Set',
        releaseDate: '2000-10',
        route: '/sets/g2'
    },
    'N1': {
        name: 'Neo Genesis',
        colors: ['#32CD32', '#FFD700', '#00CED1'],
        angle: 135,
        era: 'Neo',
        releaseDate: '2000-12',
        route: '/sets/n1'
    },
    'N2': {
        name: 'Neo Discovery',
        colors: ['#4169E1', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'Neo',
        releaseDate: '2001-09',
        route: '/sets/n2'
    },
    'N3': {
        name: 'Neo Revelation',
        colors: ['#DC143C', '#FFD700', '#8B008B'],
        angle: 135,
        era: 'Neo',
        releaseDate: '2001-09',
        route: '/sets/n3'
    },
    'N4': {
        name: 'Neo Destiny',
        colors: ['#000000', '#FFD700', '#8B0000'],
        angle: 135,
        era: 'Neo',
        releaseDate: '2002-02',
        route: '/sets/n4'
    },
    
    // ============================================
    // EX ERA
    // ============================================
    'EX1': {
        name: 'Ruby & Sapphire',
        colors: ['#DC143C', '#4169E1', '#FFD700'],
        angle: 135,
        era: 'EX',
        releaseDate: '2003-06',
        route: '/sets/ex1'
    },
    'EX2': {
        name: 'Sandstorm',
        colors: ['#D2B48C', '#8B4513', '#F4A460'],
        angle: 135,
        era: 'EX',
        releaseDate: '2003-09',
        route: '/sets/ex2'
    },
    'EX3': {
        name: 'Dragon',
        colors: ['#9932CC', '#4B0082', '#FFD700'],
        angle: 135,
        era: 'EX',
        releaseDate: '2003-11',
        route: '/sets/ex3'
    },
    'EX4': {
        name: 'Team Magma vs Team Aqua',
        colors: ['#FF4500', '#1E90FF', '#FFD700'],
        angle: 135,
        era: 'EX',
        releaseDate: '2004-03',
        route: '/sets/ex4'
    },
    'EX5': {
        name: 'Hidden Legends',
        colors: ['#228B22', '#FFD700', '#4169E1'],
        angle: 135,
        era: 'EX',
        releaseDate: '2004-06',
        route: '/sets/ex5'
    },
    'EX6': {
        name: 'FireRed & LeafGreen',
        colors: ['#DC143C', '#228B22', '#FFD700'],
        angle: 135,
        era: 'EX',
        releaseDate: '2004-09',
        route: '/sets/ex6'
    },
    'EX7': {
        name: 'Team Rocket Returns',
        colors: ['#000000', '#8B0000', '#2F2F2F'],
        angle: 135,
        era: 'EX',
        releaseDate: '2004-11',
        route: '/sets/ex7'
    },
    'EX8': {
        name: 'Deoxys',
        colors: ['#9932CC', '#FFD700', '#4169E1'],
        angle: 135,
        era: 'EX',
        releaseDate: '2005-02',
        route: '/sets/ex8'
    },
    'EX9': {
        name: 'Emerald',
        colors: ['#32CD32', '#FFD700', '#228B22'],
        angle: 135,
        era: 'EX',
        releaseDate: '2005-05',
        route: '/sets/ex9'
    },
    'EX10': {
        name: 'Unseen Forces',
        colors: ['#9370DB', '#FFD700', '#4169E1'],
        angle: 135,
        era: 'EX',
        releaseDate: '2005-08',
        route: '/sets/ex10'
    },
    'EX11': {
        name: 'Delta Species',
        colors: ['#FF6347', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'EX',
        releaseDate: '2005-10',
        route: '/sets/ex11'
    },
    'EX12': {
        name: 'Legend Maker',
        colors: ['#8B008B', '#FFD700', '#9932CC'],
        angle: 135,
        era: 'EX',
        releaseDate: '2006-02',
        route: '/sets/ex12'
    },
    'EX13': {
        name: 'Holon Phantoms',
        colors: ['#9370DB', '#00CED1', '#FFD700'],
        angle: 135,
        era: 'EX',
        releaseDate: '2006-05',
        route: '/sets/ex13'
    },
    'EX14': {
        name: 'Crystal Guardians',
        colors: ['#00CED1', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'EX',
        releaseDate: '2006-08',
        route: '/sets/ex14'
    },
    'EX15': {
        name: 'Dragon Frontiers',
        colors: ['#9932CC', '#FFD700', '#4169E1'],
        angle: 135,
        era: 'EX',
        releaseDate: '2006-11',
        route: '/sets/ex15'
    },
    'EX16': {
        name: 'Power Keepers',
        colors: ['#FF4500', '#FFD700', '#DC143C'],
        angle: 135,
        era: 'EX',
        releaseDate: '2007-02',
        route: '/sets/ex16'
    },
    
    // ============================================
    // DIAMOND & PEARL ERA
    // ============================================
    'DP': {
        name: 'Diamond & Pearl',
        colors: ['#B0C4DE', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2007-05',
        route: '/sets/dp'
    },
    'DP1': {
        name: 'Diamond & Pearl',
        colors: ['#B0C4DE', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2007-05',
        route: '/sets/dp1'
    },
    'DP2': {
        name: 'Mysterious Treasures',
        colors: ['#4B0082', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2007-08',
        route: '/sets/dp2'
    },
    'DP3': {
        name: 'Secret Wonders',
        colors: ['#9370DB', '#FFD700', '#4169E1'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2007-11',
        route: '/sets/dp3'
    },
    'DP4': {
        name: 'Great Encounters',
        colors: ['#FFD700', '#FF6347', '#9370DB'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2008-02',
        route: '/sets/dp4'
    },
    'DP5': {
        name: 'Majestic Dawn',
        colors: ['#FFD700', '#FFA500', '#9370DB'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2008-05',
        route: '/sets/dp5'
    },
    'DP6': {
        name: 'Legends Awakened',
        colors: ['#9932CC', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2008-08',
        route: '/sets/dp6'
    },
    'DP7': {
        name: 'Stormfront',
        colors: ['#708090', '#FFD700', '#2F4F4F'],
        angle: 135,
        era: 'Diamond & Pearl',
        releaseDate: '2008-11',
        route: '/sets/dp7'
    },
    
    // ============================================
    // PLATINUM ERA
    // ============================================
    'PL': {
        name: 'Platinum',
        colors: ['#C0C0C0', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'Platinum',
        releaseDate: '2009-02',
        route: '/sets/pl'
    },
    'PL1': {
        name: 'Platinum',
        colors: ['#C0C0C0', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'Platinum',
        releaseDate: '2009-02',
        route: '/sets/pl1'
    },
    'PL2': {
        name: 'Rising Rivals',
        colors: ['#FF6347', '#FFD700', '#DC143C'],
        angle: 135,
        era: 'Platinum',
        releaseDate: '2009-05',
        route: '/sets/pl2'
    },
    'PL3': {
        name: 'Supreme Victors',
        colors: ['#9932CC', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'Platinum',
        releaseDate: '2009-08',
        route: '/sets/pl3'
    },
    'PL4': {
        name: 'Arceus',
        colors: ['#FFD700', '#C0C0C0', '#9370DB'],
        angle: 135,
        era: 'Platinum',
        releaseDate: '2009-11',
        route: '/sets/pl4'
    },
    
    // ============================================
    // HEARTGOLD & SOULSILVER ERA
    // ============================================
    'HGSS': {
        name: 'HeartGold & SoulSilver',
        colors: ['#FFD700', '#FF6347', '#228B22'],
        angle: 135,
        era: 'HeartGold & SoulSilver',
        releaseDate: '2010-02',
        route: '/sets/hgss'
    },
    'HGSS1': {
        name: 'HeartGold & SoulSilver',
        colors: ['#FFD700', '#FF6347', '#228B22'],
        angle: 135,
        era: 'HeartGold & SoulSilver',
        releaseDate: '2010-02',
        route: '/sets/hgss1'
    },
    'HGSS2': {
        name: 'Unleashed',
        colors: ['#FF6347', '#FFD700', '#228B22'],
        angle: 135,
        era: 'HeartGold & SoulSilver',
        releaseDate: '2010-05',
        route: '/sets/hgss2'
    },
    'HGSS3': {
        name: 'Undaunted',
        colors: ['#8B008B', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'HeartGold & SoulSilver',
        releaseDate: '2010-08',
        route: '/sets/hgss3'
    },
    'HGSS4': {
        name: 'Triumphant',
        colors: ['#FFD700', '#9932CC', '#4B0082'],
        angle: 135,
        era: 'HeartGold & SoulSilver',
        releaseDate: '2010-11',
        route: '/sets/hgss4'
    },
    
    // ============================================
    // BLACK & WHITE ERA
    // ============================================
    'BW': {
        name: 'Black & White',
        colors: ['#424242', '#E0E0E0', '#212121'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2011-04',
        route: '/sets/bw'
    },
    'BW1': {
        name: 'Black & White',
        colors: ['#424242', '#E0E0E0', '#212121'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2011-04',
        route: '/sets/bw1'
    },
    'BW2': {
        name: 'Emerging Powers',
        colors: ['#696969', '#E0E0E0', '#2F2F2F'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2011-08',
        route: '/sets/bw2'
    },
    'BW3': {
        name: 'Noble Victories',
        colors: ['#8B0000', '#FFD700', '#2F2F2F'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2011-11',
        route: '/sets/bw3'
    },
    'BW4': {
        name: 'Next Destinies',
        colors: ['#FFD700', '#4169E1', '#2F2F2F'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2012-02',
        route: '/sets/bw4'
    },
    'BW5': {
        name: 'Dark Explorers',
        colors: ['#000000', '#8B0000', '#2F2F2F'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2012-05',
        route: '/sets/bw5'
    },
    'BW6': {
        name: 'Dragons Exalted',
        colors: ['#9932CC', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2012-08',
        route: '/sets/bw6'
    },
    'BW7': {
        name: 'Boundaries Crossed',
        colors: ['#FF6347', '#FFD700', '#228B22'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2012-11',
        route: '/sets/bw7'
    },
    'BW8': {
        name: 'Plasma Storm',
        colors: ['#1E90FF', '#FFD700', '#000080'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2013-02',
        route: '/sets/bw8'
    },
    'BW9': {
        name: 'Plasma Freeze',
        colors: ['#4169E1', '#FFD700', '#000080'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2013-05',
        route: '/sets/bw9'
    },
    'BW10': {
        name: 'Plasma Blast',
        colors: ['#1E90FF', '#FFD700', '#FF4500'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2013-08',
        route: '/sets/bw10'
    },
    'BW11': {
        name: 'Legendary Treasures',
        colors: ['#FFD700', '#9932CC', '#4B0082'],
        angle: 135,
        era: 'Black & White',
        releaseDate: '2013-11',
        route: '/sets/bw11'
    },
    
    // ============================================
    // XY ERA
    // ============================================
    'XY': {
        name: 'XY',
        colors: ['#E53935', '#1A237E', '#FFD54F'],
        angle: 135,
        era: 'XY',
        releaseDate: '2014-02',
        route: '/sets/xy'
    },
    'XY1': {
        name: 'XY',
        colors: ['#E53935', '#1A237E', '#FFD54F'],
        angle: 135,
        era: 'XY',
        releaseDate: '2014-02',
        route: '/sets/xy1'
    },
    'XY2': {
        name: 'Flashfire',
        colors: ['#DC143C', '#FF4500', '#FFD700'],
        angle: 135,
        era: 'XY',
        releaseDate: '2014-05',
        route: '/sets/xy2'
    },
    'XY3': {
        name: 'Furious Fists',
        colors: ['#FF6347', '#FF4500', '#FFD700'],
        angle: 135,
        era: 'XY',
        releaseDate: '2014-08',
        route: '/sets/xy3'
    },
    'XY4': {
        name: 'Phantom Forces',
        colors: ['#4B0082', '#9370DB', '#2F2F2F'],
        angle: 135,
        era: 'XY',
        releaseDate: '2014-11',
        route: '/sets/xy4'
    },
    'XY5': {
        name: 'Primal Clash',
        colors: ['#1E90FF', '#4169E1', '#FFD700'],
        angle: 135,
        era: 'XY',
        releaseDate: '2015-02',
        route: '/sets/xy5'
    },
    'XY6': {
        name: 'Roaring Skies',
        colors: ['#87CEEB', '#4169E1', '#FFD700'],
        angle: 135,
        era: 'XY',
        releaseDate: '2015-05',
        route: '/sets/xy6'
    },
    'XY7': {
        name: 'Ancient Origins',
        colors: ['#8B4513', '#FFD700', '#228B22'],
        angle: 135,
        era: 'XY',
        releaseDate: '2015-08',
        route: '/sets/xy7'
    },
    'XY8': {
        name: 'BREAKthrough',
        colors: ['#1E90FF', '#FFD700', '#9370DB'],
        angle: 135,
        era: 'XY',
        releaseDate: '2015-11',
        route: '/sets/xy8'
    },
    'XY9': {
        name: 'BREAKpoint',
        colors: ['#00CED1', '#4169E1', '#FFD700'],
        angle: 135,
        era: 'XY',
        releaseDate: '2016-02',
        route: '/sets/xy9'
    },
    'XY10': {
        name: 'Fates Collide',
        colors: ['#9370DB', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'XY',
        releaseDate: '2016-05',
        route: '/sets/xy10'
    },
    'XY11': {
        name: 'Steam Siege',
        colors: ['#708090', '#FFD700', '#2F4F4F'],
        angle: 135,
        era: 'XY',
        releaseDate: '2016-08',
        route: '/sets/xy11'
    },
    'XY12': {
        name: 'Evolutions',
        colors: ['#CC0000', '#FFDE00', '#003DA5'],
        angle: 135,
        era: 'XY',
        releaseDate: '2016-11',
        route: '/sets/xy12'
    },
    
    // ============================================
    // SUN & MOON ERA
    // ============================================
    'SUM': {
        name: 'Sun & Moon',
        colors: ['#FF6F00', '#0277BD', '#1B5E20'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2017-02',
        route: '/sets/sum'
    },
    'SUM1': {
        name: 'Sun & Moon',
        colors: ['#FF6F00', '#0277BD', '#1B5E20'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2017-02',
        route: '/sets/sum1'
    },
    'SUM2': {
        name: 'Guardians Rising',
        colors: ['#E65100', '#01579B', '#33691E'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2017-05',
        route: '/sets/sum2'
    },
    'SUM3': {
        name: 'Burning Shadows',
        colors: ['#DC143C', '#2F2F2F', '#8B0000'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2017-08',
        route: '/sets/sum3'
    },
    'SUM4': {
        name: 'Crimson Invasion',
        colors: ['#DC143C', '#8B0000', '#2F2F2F'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2017-11',
        route: '/sets/sum4'
    },
    'SUM5': {
        name: 'Ultra Prism',
        colors: ['#C0C0C0', '#9370DB', '#FFD700'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2018-02',
        route: '/sets/sum5'
    },
    'SUM6': {
        name: 'Forbidden Light',
        colors: ['#9370DB', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2018-05',
        route: '/sets/sum6'
    },
    'SUM7': {
        name: 'Celestial Storm',
        colors: ['#87CEEB', '#4169E1', '#FFD700'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2018-08',
        route: '/sets/sum7'
    },
    'SUM8': {
        name: 'Lost Thunder',
        colors: ['#9932CC', '#FFD700', '#4B0082'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2018-11',
        route: '/sets/sum8'
    },
    'SUM9': {
        name: 'Team Up',
        colors: ['#FF6347', '#FFD700', '#228B22'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2019-02',
        route: '/sets/sum9'
    },
    'SUM10': {
        name: 'Detective Pikachu',
        colors: ['#FFD700', '#FF6347', '#228B22'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2019-04',
        route: '/sets/sum10'
    },
    'SUM11': {
        name: 'Unbroken Bonds',
        colors: ['#FFD700', '#DC143C', '#228B22'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2019-05',
        route: '/sets/sum11'
    },
    'SUM12': {
        name: 'Unified Minds',
        colors: ['#9370DB', '#FFD700', '#4169E1'],
        angle: 135,
        era: 'Sun & Moon',
        releaseDate: '2019-08',
        route: '/sets/sum12'
    },
    
    // ============================================
    // SWORD & SHIELD ERA
    // ============================================
    'SWSH': {
        name: 'Sword & Shield',
        colors: ['#1A237E', '#E53935', '#FFD54F'],
        angle: 135,
        era: 'Sword & Shield',
        releaseDate: '2020-02',
        route: '/sets/swsh'
    },
    'SWSH1': {
        name: 'Sword & Shield',
        colors: ['#283593', '#E53935', '#FFD54F'],
        angle: 135,
        era: 'Sword & Shield',
        releaseDate: '2020-02',
        route: '/sets/swsh1'
    },
    'SWSH2': {
        name: 'Rebel Clash',
        colors: ['#1565C0', '#D32F2F', '#FFC107'],
        angle: 140,
        era: 'Sword & Shield',
        releaseDate: '2020-05',
        route: '/sets/swsh2'
    },
    'SWSH3': {
        name: 'Darkness Ablaze',
        colors: ['#0D47A1', '#C62828', '#FFB300'],
        angle: 130,
        era: 'Sword & Shield',
        releaseDate: '2020-08',
        route: '/sets/swsh3'
    },
    'SWSH4': {
        name: 'Champion\'s Path',
        colors: ['#0277BD', '#B71C1C', '#FFA000'],
        angle: 138,
        era: 'Sword & Shield',
        releaseDate: '2020-09',
        route: '/sets/swsh4'
    },
    'SWSH5': {
        name: 'Vivid Voltage',
        colors: ['#01579B', '#AD1457', '#FF8F00'],
        angle: 142,
        era: 'Sword & Shield',
        releaseDate: '2020-11',
        route: '/sets/swsh5'
    },
    'SWSH6': {
        name: 'Shining Fates',
        colors: ['#004D40', '#880E4F', '#FF6F00'],
        angle: 128,
        era: 'Sword & Shield',
        releaseDate: '2021-02',
        route: '/sets/swsh6'
    },
    'SWSH7': {
        name: 'Battle Styles',
        colors: ['#006064', '#4A148C', '#E65100'],
        angle: 136,
        era: 'Sword & Shield',
        releaseDate: '2021-03',
        route: '/sets/swsh7'
    },
    'SWSH8': {
        name: 'Chilling Reign',
        colors: ['#00796B', '#6A1B9A', '#FF5722'],
        angle: 134,
        era: 'Sword & Shield',
        releaseDate: '2021-06',
        route: '/sets/swsh8'
    },
    'SWSH9': {
        name: 'Evolving Skies',
        colors: ['#00897B', '#7B1FA2', '#FF9800'],
        angle: 132,
        era: 'Sword & Shield',
        releaseDate: '2021-08',
        route: '/sets/swsh9'
    },
    'SWSH10': {
        name: 'Fusion Strike',
        colors: ['#00695C', '#8E24AA', '#F57C00'],
        angle: 144,
        era: 'Sword & Shield',
        releaseDate: '2021-11',
        route: '/sets/swsh10'
    },
    'SWSH11': {
        name: 'Brilliant Stars',
        colors: ['#005249', '#9C27B0', '#EF6C00'],
        angle: 130,
        era: 'Sword & Shield',
        releaseDate: '2022-02',
        route: '/sets/swsh11'
    },
    'SWSH12': {
        name: 'Astral Radiance',
        colors: ['#004D40', '#AB47BC', '#E65100'],
        angle: 138,
        era: 'Sword & Shield',
        releaseDate: '2022-05',
        route: '/sets/swsh12'
    },
    'SWSH13': {
        name: 'Lost Origin',
        colors: ['#006064', '#BA68C8', '#FF6F00'],
        angle: 136,
        era: 'Sword & Shield',
        releaseDate: '2022-09',
        route: '/sets/swsh13'
    },
    'SWSH14': {
        name: 'Silver Tempest',
        colors: ['#C0C0C0', '#9370DB', '#FFD700'],
        angle: 135,
        era: 'Sword & Shield',
        releaseDate: '2022-11',
        route: '/sets/swsh14'
    },
    
    // ============================================
    // SCARLET & VIOLET ERA
    // ============================================
    'SVE': {
        name: 'Scarlet & Violet',
        colors: ['#D32F2F', '#1976D2', '#388E3C'],
        angle: 135,
        era: 'Scarlet & Violet',
        releaseDate: '2023-03',
        route: '/sets/sve'
    },
    'SVI': {
        name: 'Scarlet & Violet',
        colors: ['#C62828', '#1565C0', '#2E7D32'],
        angle: 135,
        era: 'Scarlet & Violet',
        releaseDate: '2023-03',
        route: '/sets/svi'
    },
    'SVI1': {
        name: 'Scarlet & Violet',
        colors: ['#D32F2F', '#1976D2', '#388E3C'],
        angle: 135,
        era: 'Scarlet & Violet',
        releaseDate: '2023-03',
        route: '/sets/svi1'
    },
    'SVI2': {
        name: 'Paldea Evolved',
        colors: ['#AD1457', '#0D47A1', '#1B5E20'],
        angle: 140,
        era: 'Scarlet & Violet',
        releaseDate: '2023-06',
        route: '/sets/svi2'
    },
    'SVI3': {
        name: 'Obsidian Flames',
        colors: ['#880E4F', '#0277BD', '#33691E'],
        angle: 130,
        era: 'Scarlet & Violet',
        releaseDate: '2023-08',
        route: '/sets/svi3'
    },
    'SVI4': {
        name: '151',
        colors: ['#6A1B9A', '#01579B', '#558B2F'],
        angle: 138,
        era: 'Scarlet & Violet',
        releaseDate: '2023-09',
        route: '/sets/svi4'
    },
    'SVI5': {
        name: 'Paradox Rift',
        colors: ['#4A148C', '#004D40', '#689F38'],
        angle: 142,
        era: 'Scarlet & Violet',
        releaseDate: '2023-11',
        route: '/sets/svi5'
    },
    'SVI6': {
        name: 'Paldean Fates',
        colors: ['#7B1FA2', '#006064', '#827717'],
        angle: 128,
        era: 'Scarlet & Violet',
        releaseDate: '2024-01',
        route: '/sets/svi6'
    },
    'SVI7': {
        name: 'Temporal Forces',
        colors: ['#8E24AA', '#00796B', '#33691E'],
        angle: 136,
        era: 'Scarlet & Violet',
        releaseDate: '2024-03',
        route: '/sets/svi7'
    },
    'SVI8': {
        name: 'Twilight Masquerade',
        colors: ['#9C27B0', '#009688', '#558B2F'],
        angle: 134,
        era: 'Scarlet & Violet',
        releaseDate: '2024-05',
        route: '/sets/svi8'
    },
    'SVI9': {
        name: 'Shrouded Fable',
        colors: ['#AB47BC', '#00897B', '#689F38'],
        angle: 132,
        era: 'Scarlet & Violet',
        releaseDate: '2024-08',
        route: '/sets/svi9'
    },
    
    // ============================================
    // DEFAULT FALLBACK
    // ============================================
    'default': {
        name: 'Default',
        colors: ['#CC0000', '#FFDE00', '#003DA5'],
        angle: 135,
        era: 'Unknown',
        releaseDate: '1900-01',
        route: '/sets/default'
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = POKEMON_TCG_SET_THEMES;
}
