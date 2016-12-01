module.exports = {
    entry : {
        index : "./index.js"
    },
    output : {
        path : "./build",
        filename : "bundle.js"
    },
    module : {
        loaders :[
            {
                test: /\.js?$/,
                exclude:/(node_modules|bower_components)/,
                loader: 'babel',
                query  :{
                    presets:['react','es2015']
                }
            },
        ]

    }
}