const getPortfolioAssetPairs = (currency, data) => {
    let baseCurrency = null;
    let assetPairs = [];
    for (let account of data.accounts) {
        for (let asset of data.assets) {
            if (asset.display && (account.name === asset.name)) {
                // asset.display is type String of tradeCurrency/baseCurrency format
                baseCurrency = asset.display.split('/')[1];
                if (baseCurrency.includes(currency) && baseCurrency === currency) {
                    assetPairs.push(asset.display);
                }
            }
        }
    }
    return assetPairs;
};
