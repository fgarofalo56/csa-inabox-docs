/**
 * Infrastructure layer for logging
 * Provides structured logging with different levels and outputs
 */
import winston from 'winston';
import chalk from 'chalk';
import path from 'path';

export class Logger {
  constructor(options = {}) {
    this.options = {
      level: options.level || 'info',
      logFile: options.logFile || null,
      colorize: options.colorize !== false,
      timestamp: options.timestamp !== false,
      ...options
    };

    this.winston = this.createWinstonLogger();
  }

  /**
   * Create Winston logger instance
   * @returns {winston.Logger} - Configured Winston logger
   */
  createWinstonLogger() {
    const formats = [winston.format.errors({ stack: true })];

    if (this.options.timestamp) {
      formats.push(winston.format.timestamp());
    }

    const consoleFormat = winston.format.printf(({ level, message, timestamp, stack }) => {
      const time = timestamp ? `${timestamp} ` : '';
      const msg = stack || message;
      return `${time}[${level.toUpperCase()}] ${msg}`;
    });

    const transports = [
      new winston.transports.Console({
        format: winston.format.combine(
          winston.format.colorize({ all: this.options.colorize }),
          consoleFormat
        )
      })
    ];

    if (this.options.logFile) {
      transports.push(
        new winston.transports.File({
          filename: this.options.logFile,
          format: winston.format.combine(
            winston.format.timestamp(),
            winston.format.json()
          )
        })
      );
    }

    return winston.createLogger({
      level: this.options.level,
      format: winston.format.combine(...formats),
      transports
    });
  }

  /**
   * Log info message
   * @param {string} message - Message to log
   * @param {object} meta - Additional metadata
   */
  info(message, meta = {}) {
    this.winston.info(message, meta);
  }

  /**
   * Log warning message
   * @param {string} message - Message to log
   * @param {object} meta - Additional metadata
   */
  warn(message, meta = {}) {
    this.winston.warn(message, meta);
  }

  /**
   * Log error message
   * @param {string} message - Message to log
   * @param {object} meta - Additional metadata
   */
  error(message, meta = {}) {
    this.winston.error(message, meta);
  }

  /**
   * Log debug message
   * @param {string} message - Message to log
   * @param {object} meta - Additional metadata
   */
  debug(message, meta = {}) {
    this.winston.debug(message, meta);
  }

  /**
   * Log verbose message
   * @param {string} message - Message to log
   * @param {object} meta - Additional metadata
   */
  verbose(message, meta = {}) {
    this.winston.verbose(message, meta);
  }

  /**
   * Log success message with green color
   * @param {string} message - Message to log
   */
  success(message) {
    console.log(this.options.colorize ? chalk.green(`✅ ${message}`) : `✅ ${message}`);
  }

  /**
   * Log failure message with red color
   * @param {string} message - Message to log
   */
  failure(message) {
    console.log(this.options.colorize ? chalk.red(`❌ ${message}`) : `❌ ${message}`);
  }

  /**
   * Log progress message with blue color
   * @param {string} message - Message to log
   */
  progress(message) {
    console.log(this.options.colorize ? chalk.blue(`🔄 ${message}`) : `🔄 ${message}`);
  }

  /**
   * Log section header
   * @param {string} title - Section title
   */
  section(title) {
    const separator = '='.repeat(Math.min(60, title.length + 20));
    console.log();
    console.log(this.options.colorize ? chalk.bold.cyan(separator) : separator);
    console.log(this.options.colorize ? chalk.bold.cyan(`📊 ${title}`) : `📊 ${title}`);
    console.log(this.options.colorize ? chalk.bold.cyan(separator) : separator);
    console.log();
  }

  /**
   * Log subsection header
   * @param {string} title - Subsection title
   */
  subsection(title) {
    console.log();
    console.log(this.options.colorize ? chalk.bold.yellow(`🔍 ${title}`) : `🔍 ${title}`);
    console.log(this.options.colorize ? chalk.gray('-'.repeat(40)) : '-'.repeat(40));
  }

  /**
   * Log summary statistics
   * @param {object} stats - Statistics object
   */
  summary(stats) {
    console.log();
    console.log(this.options.colorize ? chalk.bold.magenta('📈 SUMMARY:') : '📈 SUMMARY:');
    
    Object.entries(stats).forEach(([key, value]) => {
      const formattedKey = key.replace(/([A-Z])/g, ' $1').toLowerCase();
      const capitalizedKey = formattedKey.charAt(0).toUpperCase() + formattedKey.slice(1);
      console.log(`   ${capitalizedKey}: ${value}`);
    });
  }

  /**
   * Log table data
   * @param {object[]} data - Array of objects to display as table
   * @param {string[]} columns - Column names to display
   */
  table(data, columns = null) {
    if (data.length === 0) return;

    const cols = columns || Object.keys(data[0]);
    console.table(data, cols);
  }

  /**
   * Log with custom emoji and color
   * @param {string} emoji - Emoji to use
   * @param {string} message - Message to log
   * @param {string} color - Chalk color name
   */
  custom(emoji, message, color = null) {
    const text = `${emoji} ${message}`;
    console.log(this.options.colorize && color ? chalk[color](text) : text);
  }

  /**
   * Create progress bar logger
   * @param {string} title - Progress bar title
   * @returns {object} - Progress bar interface
   */
  createProgressBar(title) {
    let current = 0;
    let total = 0;
    let lastMessage = '';

    return {
      start: (totalItems, message = '') => {
        total = totalItems;
        current = 0;
        lastMessage = message;
        console.log(this.options.colorize ? chalk.blue(`🚀 ${title}`) : `🚀 ${title}`);
      },
      
      update: (currentItem, message = '') => {
        current = currentItem;
        lastMessage = message || lastMessage;
        const percentage = Math.round((current / total) * 100);
        const progress = '█'.repeat(Math.round(percentage / 5));
        const empty = '░'.repeat(20 - Math.round(percentage / 5));
        const bar = `[${progress}${empty}] ${percentage}%`;
        
        process.stdout.write(`\r${bar} ${current}/${total} - ${lastMessage}`);
      },
      
      finish: (message = 'Complete!') => {
        process.stdout.write('\n');
        this.success(`${title} - ${message}`);
      },
      
      fail: (message = 'Failed!') => {
        process.stdout.write('\n');
        this.failure(`${title} - ${message}`);
      }
    };
  }

  /**
   * Set log level
   * @param {string} level - Log level (error, warn, info, verbose, debug)
   */
  setLevel(level) {
    this.winston.level = level;
  }

  /**
   * Create child logger with additional context
   * @param {object} context - Additional context for all log messages
   * @returns {Logger} - Child logger instance
   */
  child(context) {
    const childLogger = new Logger({
      ...this.options,
      logFile: null // Don't duplicate file logging
    });
    
    // Override winston instance to include context
    const originalWinston = childLogger.winston;
    childLogger.winston = {
      info: (message, meta = {}) => originalWinston.info(message, { ...context, ...meta }),
      warn: (message, meta = {}) => originalWinston.warn(message, { ...context, ...meta }),
      error: (message, meta = {}) => originalWinston.error(message, { ...context, ...meta }),
      debug: (message, meta = {}) => originalWinston.debug(message, { ...context, ...meta }),
      verbose: (message, meta = {}) => originalWinston.verbose(message, { ...context, ...meta })
    };
    
    return childLogger;
  }
}