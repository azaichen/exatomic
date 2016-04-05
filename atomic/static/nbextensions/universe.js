/*"""
=========================================================
Universe View
=========================================================
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/container': {
            exports: 'container'
        },

        'nbextensions/exa/atomic/app': {
            exports: 'app'
        },

        'nbextensions/exa/atomic/test': {
            exports: 'test'
        },
    },
});


define([
    'widgets/js/widget',
    'nbextensions/exa/container',
    'nbextensions/exa/atomic/app'
], function(widget, container, app){
    class UniverseView extends container.ContainerView {
        /*"""
        UniverseView
        ================
        */
        if_test() {
            var check = this.get_trait('test');
            if (check === true) {
                console.log('Empty universe, displaying testing interface');
                this.app = new test.TestApp(this);
            };
        };
    };
        render: function() {
            /*"""
            render
            --------------
            Main entry point for the universe container frontend.
            */
            console.log('Initializing universe...');
            var self = this;
            this.init_default_model_listeners();
            this.init_listeners();

            this.init_container();
            this.init_canvas(this.gui_width);
            this.app = new app.AtomicApp(this);

            this.container.append(this.canvas);       // Lastly set the html
            this.container.append(this.app.gui.domElement);
            this.container.append(this.app.gui_style);
            this.setElement(this.container);          // objects and run.
            this.app.app3d.render();
            this.on('displayed', function() {
                self.app.app3d.animate();
                self.app.app3d.controls.handleResize();
            });
        },

        init_listeners: function() {
            /*"""
            init_listeners
            ---------------
            Set up the frontend to listen for changes on the backend
            */
            this.update_atom_x();
            this.update_atom_y();
            this.update_atom_z();
            this.update_atom_radii_dict();
            this.update_atom_colors_dict();
            this.update_atom_symbols();
            this.update_framelist();
            this.update_two_bond0();
            this.update_two_bond1();
            this.model.on('change:atom_x', this.update_x, this);
            this.model.on('change:atom_y', this.update_y, this);
            this.model.on('change:atom_z', this.update_z, this);
            this.model.on('change:atom_radii', this.update_atom_radii_dict, this);
            this.model.on('change:atom_colors', this.update_atom_colors_dict, this);
            this.model.on('change:atom_symbols', this.update_atom_symbols, this);
            this.model.on('change:frame_frame', this.update_framelist, this);
            this.model.on('change:two_bond0', this.update_two_bond0, this);
            this.model.on('change:two_bond1', this.update_two_bond1, this);
        },

        update_atom_x: function() {
            /*"""
            update_atom_x
            -----------
            Updates x component of nuclear coordinates.
            */
            this.atom_x = this.get_trait('atom_x');
        },

        update_atom_y: function() {
            /*"""
            update_atom_y
            -----------
            Updates y component of nuclear coordinates.
            */
            this.atom_y = this.get_trait('atom_y');
        },

        update_atom_z: function() {
            /*"""
            update_atom_z
            -----------
            Updates z component of nuclear coordinates.
            */
            this.atom_z = this.get_trait('atom_z');
        },

        update_framelist: function() {
            this.framelist = this.get_trait('frame_frame');
        },

        update_atom_symbols: function() {
            this.atom_symbols = this.get_trait('atom_symbols');
        },

        update_atom_radii_dict: function() {
            this.atom_radii_dict = this.get_trait('atom_radii');
        },

        update_atom_colors_dict: function() {
            this.atom_colors_dict = this.get_trait('atom_colors');
        },

        update_two_bond0: function() {
            this.two_bond0 = this.get_trait('two_bond0');
        },

        update_two_bond1: function() {
            this.two_bond1 = this.get_trait('two_bond1');
        },
    });

    return {'UniverseView': UniverseView};
});
