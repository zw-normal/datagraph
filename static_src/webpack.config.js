const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: {
        'sb-admin-2': './src/datagraph/sb-admin-2.ts',
        'engine-workbench': './src/engine/workbench/index.ts',
        'engine-node-editor': './src/engine/node-editor/index.ts',
        'engine-spreadsheet-widget': './src/engine/spreadsheet-widget/index.ts',
        'viewer-browser': './src/viewer/browser/index.ts',
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, '../static_build/datagraph'),
    },
    resolve: {
        extensions: [ '.tsx', '.ts', '.js' ],
        alias: {
            vue: 'vue/dist/vue.js'
        },
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    // Creates `style` nodes from JS strings
                    'style-loader',
                    // Translates CSS into CommonJS
                    'css-loader',
                    // Compiles Sass to CSS
                    'sass-loader',
                ],
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
    ]
};
