module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                src: 'flask_covid19/<%= pkg.name %>.js',
                dest: 'build/<%= pkg.name %>.min.js'
            }
        },
        sass: {
            dist: {
                files: {
                    'node_modules/jquery-fancybox/source/css/jquery.fancybox.css': 'node_modules/jquery-fancybox/source/scss/jquery.fancybox.scss'
                }
            }
        },
        copy: {
            main: {
                files: [
                    {expand: true, cwd: 'node_modules/jquery/dist/', src: ['**'], dest: 'static/vendor/jquery'},
                    {expand: true, cwd: 'node_modules/popper.js/dist/', src: ['**'], dest: 'static/vendor/popper.js'},
                    {expand: true, cwd: 'node_modules/bootstrap/dist/', src: ['**'], dest: 'static/vendor/bootstrap'},
                    {expand: true, cwd: 'node_modules/@fortawesome/fontawesome-free/', src: ['**'], dest: 'static/vendor/fontawesome-free'},
                    {expand: true, cwd: 'node_modules/bootswatch/dist/', src: ['**'], dest: 'static/vendor/bootswatch'},
                ],
            },
        },
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-run-grunt');
    grunt.loadNpmTasks('grunt-contrib-versioning2');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-copy');

    // Default task(s).
    grunt.registerTask('default', ['copy']);

    // https://www.npmjs.com/package/grunt-contrib-copy
    // https://www.npmjs.com/package/grunt-contrib-jshint
    // https://www.npmjs.com/package/grunt-contrib-clean
    // https://www.npmjs.com/package/grunt-contrib-sass
};
