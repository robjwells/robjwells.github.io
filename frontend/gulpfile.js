// Imports
var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),  // vendor prefixes
    changed = require('gulp-changed'),            // changed files only
    concat = require('gulp-concat'),              // concatenate
    csso = require('gulp-csso'),                  // minify
    rename = require('gulp-rename'),              // rename file
    replace = require('gulp-replace'),            // regex substitution
    uglify = require('gulp-uglify');              // UglifyJS


// Directories
var css_dir = 'css/',
    css_glob = css_dir + '*.css',
    js_dir = 'js/',
    js_glob = 'js/*.js',
    build_dir = 'build/';


gulp.task('css', gulp.series(function (done) {
    // Imports are removed because we're explicity concatenating.
    // The imports in those files are really a development convenience.
    // The order of filenames in ordered_files is important.

    var ordered_files = ['reset', 'styles', 'highlight'].map(function (name) {
        return css_dir + name + '.css';
    });

    gulp.src(ordered_files)
        .pipe(replace(/@charset\ .+\n/, ''))  // remove charset declarations
        .pipe(replace(/@import\ .+\n/, ''))   // remove imports
        .pipe(autoprefixer())
        .pipe(concat('all.css'))
        .pipe(replace(/^/, "@charset 'utf-8';\n")) // add back single charset
        .pipe(replace(/\/\*![^\n]+/g, ''))         // remove comments
        .pipe(gulp.dest(build_dir))
        .pipe(csso())  // minify
        .pipe(rename('all.min.css'))
        .pipe(gulp.dest(build_dir));

    done();
}));


gulp.task('js', gulp.series(function (done) {
    // The order of filenames in ordered_files is important
    var ordered_files = ['robjwells'].map(function (name) {
        return js_dir + name + '.js';
    });

    gulp.src(ordered_files)
        .pipe(concat('all.js'))
        .pipe(gulp.dest(build_dir))
        .pipe(uglify())
        .pipe(rename('all.min.js'))
        .pipe(gulp.dest(build_dir));

    done();
}));


gulp.task('watch', gulp.series(function (done) {
    gulp.watch(css_glob, ['css']);
    gulp.watch(js_glob, ['js']);
    done();
}));


gulp.task('default', gulp.series(['css', 'js']));
