const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: {
        'sb-admin-2': './src/datanestgraph/sb-admin-2.ts',
        'dataengine-workbench': './src/dataengine/workbench/index.ts',
        'dataengine-node-editor': './src/dataengine/node-editor/index.ts',
        'dataengine-spreadsheet-widget': './src/dataengine/spreadsheet-widget/index.ts',
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, '../static_build/datanestgraph'),
    },
    resolve: {
        extensions: [ '.tsx', '.ts', '.js' ],
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
