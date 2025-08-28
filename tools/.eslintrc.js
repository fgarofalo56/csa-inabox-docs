module.exports = {
  env: {
    es2022: true,
    node: true,
    jest: true
  },
  extends: [
    'eslint:recommended',
    'prettier'
  ],
  plugins: [
    'node'
  ],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module'
  },
  rules: {
    // Error prevention
    'no-unused-vars': ['error', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_' 
    }],
    'no-console': 'off', // Allow console in CLI tools
    'no-process-exit': 'off', // Allow process.exit in CLI
    
    // Node.js specific
    'node/no-missing-import': 'off', // Handled by module resolution
    'node/no-unpublished-import': 'off', // Allow dev dependencies in tests
    
    // Code quality
    'prefer-const': 'error',
    'no-var': 'error',
    'object-shorthand': 'error',
    'prefer-template': 'error',
    'template-curly-spacing': ['error', 'never'],
    
    // ES6+ features
    'arrow-spacing': 'error',
    'no-duplicate-imports': 'error',
    'prefer-arrow-callback': 'error',
    
    // Error handling
    'no-throw-literal': 'error',
    'prefer-promise-reject-errors': 'error'
  },
  overrides: [
    {
      files: ['tests/**/*.js', '**/*.test.js', '**/*.spec.js'],
      env: {
        jest: true
      },
      rules: {
        'no-unused-expressions': 'off' // Allow chai/jest assertions
      }
    },
    {
      files: ['src/bin/*.js'],
      rules: {
        'no-process-exit': 'off', // Allow process.exit in CLI entry points
        'no-console': 'off' // Allow console output in CLI
      }
    }
  ]
};