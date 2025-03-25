"use strict";
(self["webpackChunkegi_jupyterlab_ext"] = self["webpackChunkegi_jupyterlab_ext"] || []).push([["lib_index_js"],{

/***/ "./lib/components/NumberInput.js":
/*!***************************************!*\
  !*** ./lib/components/NumberInput.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ NumberInput)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../widget */ "./lib/widget.js");



function NumberInput({ 
// currentRefreshValue,
handleRefreshNumberChange }) {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { id: "outlined-number", label: "Refresh(S)", type: "number", slotProps: {
            inputLabel: {
                shrink: true
            }
        }, onChange: event => handleRefreshNumberChange(event.target.value), 
        // value={currentRefreshValue}
        defaultValue: _widget__WEBPACK_IMPORTED_MODULE_2__.DEFAULT_REFRESH_RATE, size: "small", sx: { maxWidth: 90 } }));
}


/***/ }),

/***/ "./lib/components/RefreshButton.js":
/*!*****************************************!*\
  !*** ./lib/components/RefreshButton.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ RefreshButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_RefreshRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/RefreshRounded */ "./node_modules/@mui/icons-material/esm/RefreshRounded.js");



function RefreshButton({ handleRefreshClick }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleRefreshClick, size: "small" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_RefreshRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null))));
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");



/**
 * Main reference: https://github.com/jupyterlab/extension-examples/blob/71486d7b891175fb3883a8b136b8edd2cd560385/react/react-widget/src/index.ts
 * And all other files in the repo.
 */
const namespaceId = 'gdapod';
/**
 * Initialization data for the GreenDIGIT JupyterLab extension.
 */
const plugin = {
    id: 'jupyterlab-greendigit',
    description: 'GreenDIGIT App',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: async (app, palette, restorer) => {
        console.log('JupyterLab extension GreenDIGIT is activated!');
        const { shell } = app;
        // Create a widget tracker
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: namespaceId
        });
        // Ensure the tracker is restored properly on refresh
        restorer.restore(tracker, {
            command: `${namespaceId}:open`,
            name: () => 'greendigit-jupyterlab'
            // when: app.restored, // Ensure restorer waits for the app to be fully restored
        });
        // Define a widget creator function
        const newWidget = async () => {
            const content = new _widget__WEBPACK_IMPORTED_MODULE_2__.MainWidget();
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.id = 'greendigit-jupyterlab';
            widget.title.label = 'GreenDIGIT Dashboard';
            widget.title.closable = true;
            return widget;
        };
        // Add an application command
        const openCommand = `${namespaceId}:open`;
        app.commands.addCommand(openCommand, {
            label: 'Open GreenDIGIT Dashboard',
            execute: async () => {
                let widget = tracker.currentWidget;
                if (!widget || widget.isDisposed) {
                    widget = await newWidget();
                    // Add the widget to the tracker and shell
                    tracker.add(widget);
                    shell.add(widget, 'main');
                }
                if (!widget.isAttached) {
                    shell.add(widget, 'main');
                }
                shell.activateById(widget.id);
            }
        });
        // Add the command to the palette
        palette.addItem({ command: openCommand, category: 'Sustainability' });
        // Restore the widget if available
        if (!tracker.currentWidget) {
            const widget = await newWidget();
            tracker.add(widget);
            shell.add(widget, 'main');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DEFAULT_REFRESH_RATE: () => (/* binding */ DEFAULT_REFRESH_RATE),
/* harmony export */   MainWidget: () => (/* binding */ MainWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _components_RefreshButton__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/RefreshButton */ "./lib/components/RefreshButton.js");
/* harmony import */ var _components_NumberInput__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/NumberInput */ "./lib/components/NumberInput.js");





// import BandHighLight from './components/BandHighLight';
// import ElementHighlights from './components/ElementHighlights';
// import MapComponent from './components/map/MapComponent';
// import VerticalLinearStepper from './components/VerticalLinearStepper';
const styles = {
    main: {
        display: 'flex',
        flexDirection: 'row',
        width: '100%',
        height: '100%',
        flexWrap: 'wrap',
        boxSizing: 'border-box',
        padding: '3px'
    },
    grid: {
        display: 'flex',
        justifyContent: 'center',
        // alignItems: 'center',
        flex: '0 1 100%',
        width: '100%'
    }
};
// function GridContent() {
//   return (
//     <Grid2 sx={{ width: '100%', px: 3, py: 5 }}>
//       <VerticalLinearStepper />
//     </Grid2>
//   );
// }
const DEFAULT_REFRESH_RATE = 2;
function debounce(func, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => func(...args), delay);
    };
}
/**
 * React component for a counter.
 *
 * @returns The React component
 */
const App = () => {
    const iframeRef = react__WEBPACK_IMPORTED_MODULE_0___default().useRef(null);
    const [refreshRateS, setRefreshRateS] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(DEFAULT_REFRESH_RATE);
    const [iframeSrc, setIframeSrc] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(`http://localhost:3000/d-solo/ceetwcgabhgcgb/ping-go-server?orgId=1&from=1741098858351&to=1741100658351&timezone=browser&panelId=1&__feature.dashboardSceneSolo&refresh=${refreshRateS}s`);
    react__WEBPACK_IMPORTED_MODULE_0___default().useEffect(() => {
        setIframeSrc(prevState => {
            const base = prevState.split('&refresh=')[0];
            return `${base}&refresh=${refreshRateS}s`;
        });
    }, [refreshRateS]);
    function handleRefreshClick() {
        // alert('Refreshing...');
        if (iframeRef.current) {
            const copy_src = structuredClone(iframeRef.current.src);
            iframeRef.current.src = copy_src;
        }
    }
    // function handleNumberChange(value: string) {
    //   debounce(() => setRefreshRateS(Number(value)), 200);
    // }
    // Create a debounced version of setRefreshRateS
    // Using 200ms delay instead of 2ms for a noticeable debounce effect.
    const debouncedSetRefreshRateS = react__WEBPACK_IMPORTED_MODULE_0___default().useMemo(() => debounce((value) => setRefreshRateS(value), 1000), []);
    // Call the debounced function on number change
    function handleNumberChange(value) {
        const parsedValue = Number(value);
        if (!isNaN(parsedValue)) {
            debouncedSetRefreshRateS(parsedValue);
        }
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: styles.main },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Paper, { style: styles.grid },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("iframe", { src: iframeSrc, width: "450", height: "200", frameBorder: "0", sandbox: "allow-scripts allow-same-origin", ref: iframeRef }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Grid2, null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_RefreshButton__WEBPACK_IMPORTED_MODULE_3__["default"], { handleRefreshClick: handleRefreshClick }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_NumberInput__WEBPACK_IMPORTED_MODULE_4__["default"]
                // currentRefreshValue={refreshRateS}
                , { 
                    // currentRefreshValue={refreshRateS}
                    handleRefreshNumberChange: newValue => handleNumberChange(newValue) })))));
};
/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
class MainWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Constructs a new CounterWidget.
     */
    constructor() {
        super();
        this.addClass('jp-ReactWidget');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(App, null);
    }
}


/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/RefreshRounded.js":
/*!****************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/RefreshRounded.js ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M17.65 6.35c-1.63-1.63-3.94-2.57-6.48-2.31-3.67.37-6.69 3.35-7.1 7.02C3.52 15.91 7.27 20 12 20c3.19 0 5.93-1.87 7.21-4.56.32-.67-.16-1.44-.9-1.44-.37 0-.72.2-.88.53-1.13 2.43-3.84 3.97-6.8 3.31-2.22-.49-4.01-2.3-4.48-4.52C5.31 9.44 8.26 6 12 6c1.66 0 3.14.69 4.22 1.78l-1.51 1.51c-.63.63-.19 1.71.7 1.71H19c.55 0 1-.45 1-1V6.41c0-.89-1.08-1.34-1.71-.71z"
}), 'RefreshRounded'));

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0ed439fa35632397ee3b.js.map