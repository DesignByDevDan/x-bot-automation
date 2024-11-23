const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './src/index.js', // Entry point for your app
    output: {
        path: path.resolve(__dirname, 'dist'), // Output folder
        filename: 'bundle.js', // Bundled file name
    },
    mode: 'development', // Use 'production' for production builds
    devServer: {
        static: {
            directory: path.join(__dirname, 'public'), // Folder for static files
        },
        port: 3000, // Port for the dev server
        hot: true, // Enable hot module replacement
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/, // Apply Babel loader to JS and JSX files
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
            {
                test: /\.css$/, // Load CSS files
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|jpg|gif|svg)$/, // Load image files
                type: 'asset/resource',
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx'], // Resolve these file extensions
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html', // Path to your HTML template
        }),
    ],
};
