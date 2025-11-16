module.exports = [
    {
        files: ["*.js"],
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: "script"
        },
        rules: {
            "no-unused-vars": "warn",
            "no-console": "warn",
            "eqeqeq": "error",
            "curly": "error"
        }
    }
];