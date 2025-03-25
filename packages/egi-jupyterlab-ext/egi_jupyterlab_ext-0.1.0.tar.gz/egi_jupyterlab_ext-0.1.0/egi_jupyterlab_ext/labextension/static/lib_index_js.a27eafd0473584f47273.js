"use strict";
(self["webpackChunkegi_jupyterlab_ext"] = self["webpackChunkegi_jupyterlab_ext"] || []).push([["lib_index_js"],{

/***/ "./lib/components/VerticalLinearStepper.js":
/*!*************************************************!*\
  !*** ./lib/components/VerticalLinearStepper.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ VerticalLinearStepper)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_Stepper__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/Stepper */ "./node_modules/@mui/material/Stepper/Stepper.js");
/* harmony import */ var _mui_material_Step__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/material/Step */ "./node_modules/@mui/material/Step/Step.js");
/* harmony import */ var _mui_material_StepLabel__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material/StepLabel */ "./node_modules/@mui/material/StepLabel/StepLabel.js");
/* harmony import */ var _mui_material_StepContent__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material/StepContent */ "./node_modules/@mui/material/StepContent/StepContent.js");
/* harmony import */ var _mui_material_Button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/Button.js");
/* harmony import */ var _mui_material_Paper__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @mui/material/Paper */ "./node_modules/@mui/material/Paper/Paper.js");
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _progress_CircularWithValueLabel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./progress/CircularWithValueLabel */ "./lib/components/progress/CircularWithValueLabel.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _table_CollapsibleTable__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./table/CollapsibleTable */ "./lib/components/table/CollapsibleTable.js");
/* harmony import */ var _progress_LinearProgress__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./progress/LinearProgress */ "./lib/components/progress/LinearProgress.js");













const steps = [
    {
        label: 'Approach'
    },
    {
        label: 'Fetch/compute',
        hasButtons: false
    },
    {
        label: 'Visualisation options'
    },
    {
        label: 'Deployment',
        hasButtons: false
    }
];
function StepOne() {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControl, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.RadioGroup, { "aria-labelledby": "demo-radio-buttons-group-label", defaultValue: "pre-compute", name: "radio-buttons-group" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControlLabel, { value: "pre-compute", control: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Radio, null), label: "Pre-Compute" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControlLabel, { value: "sample", control: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Radio, null), label: "Sample Computation" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.FormControlLabel, { value: "simulation-pred", control: react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Radio, null), label: "Simulation/Prediction" })))));
}
function StepTwo({ handleFinish, label }) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], null, label),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_progress_CircularWithValueLabel__WEBPACK_IMPORTED_MODULE_3__["default"], { onFinish: handleFinish })));
}
function StepThree() {
    return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null);
}
function StepFour({ handleFinish, label }) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { onClick: handleFinish, title: "Reset" })));
}
function ContentHandler({ step, triggerNextStep, handleLastStep }) {
    switch (step) {
        default:
        case 0:
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepOne, null);
        case 1:
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepTwo, { handleFinish: triggerNextStep, label: "Predicting results..." }));
        case 2:
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepThree, null);
        case 3:
            return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(StepFour, { handleFinish: handleLastStep, label: "Deploying application..." }));
    }
}
function VerticalLinearStepper() {
    const [activeStep, setActiveStep] = react__WEBPACK_IMPORTED_MODULE_0__.useState(0);
    const [complete, setComplete] = react__WEBPACK_IMPORTED_MODULE_0__.useState(false);
    const [checkedIndex, setCheckedIndex] = react__WEBPACK_IMPORTED_MODULE_0__.useState(null);
    const disableNextStepThree = activeStep === 2 && checkedIndex === null;
    const handleNext = () => {
        setActiveStep(prevActiveStep => prevActiveStep + 1);
    };
    const handleBack = () => {
        setActiveStep(prevActiveStep => prevActiveStep - (prevActiveStep === 2 ? 2 : 1));
    };
    const handleReset = () => {
        setActiveStep(0);
        setComplete(false);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', width: '100%', height: '500px' } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Stepper__WEBPACK_IMPORTED_MODULE_5__["default"], { activeStep: activeStep, orientation: "vertical" }, steps.map((step, index) => (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Step__WEBPACK_IMPORTED_MODULE_6__["default"], { key: step.label },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_StepLabel__WEBPACK_IMPORTED_MODULE_7__["default"], { optional: index === steps.length - 1 ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "caption" }, "Last step")) : null }, step.label),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_StepContent__WEBPACK_IMPORTED_MODULE_8__["default"], null,
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement(ContentHandler, { step: activeStep, triggerNextStep: handleNext, handleLastStep: handleReset }),
                    step.hasButtons !== false && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_9__["default"], { sx: { mb: 2 } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "contained", onClick: handleNext, sx: { mt: 1, mr: 1 }, disabled: disableNextStepThree }, index === steps.length - 1 ? 'Finish' : 'Continue'),
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { disabled: index === 0, onClick: handleBack, sx: { mt: 1, mr: 1 } }, "Back"))))))))),
        activeStep === 2 && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Paper__WEBPACK_IMPORTED_MODULE_10__["default"], { square: true, elevation: 0, sx: { p: 3, width: '100%', overflow: 'visible' } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_table_CollapsibleTable__WEBPACK_IMPORTED_MODULE_11__["default"], { checkedIndex: checkedIndex, setCheckedIndex: setCheckedIndex }))),
        activeStep === 3 && (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { width: '400px' } }, complete ? (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', justifyContent: 'center' } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], null, "Deployment complete!"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_4__["default"], { title: "Reset", onClick: handleReset }))) : (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_2__["default"], null, "Deploying..."),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_progress_LinearProgress__WEBPACK_IMPORTED_MODULE_12__["default"], { setComplete: () => setComplete(true) })))))));
}


/***/ }),

/***/ "./lib/components/progress/CircularWithValueLabel.js":
/*!***********************************************************!*\
  !*** ./lib/components/progress/CircularWithValueLabel.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CircularWithValueLabel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/CircularProgress */ "./node_modules/@mui/material/CircularProgress/CircularProgress.js");
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");




function CircularProgressWithLabel(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { position: 'relative', display: 'inline-flex' } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "determinate", ...props }),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "caption", component: "div", sx: { color: 'text.secondary' } }, `${Math.round(props.value)}%`))));
}
function CircularWithValueLabel({ onFinish }) {
    const [progress, setProgress] = react__WEBPACK_IMPORTED_MODULE_0__.useState(10);
    function handleConclusion() {
        onFinish();
        return 0;
    }
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        const timer = setInterval(() => {
            setProgress(prevProgress => prevProgress >= 100 ? handleConclusion() : prevProgress + 10);
        }, 400);
        return () => {
            clearInterval(timer);
        };
    }, []);
    return react__WEBPACK_IMPORTED_MODULE_0__.createElement(CircularProgressWithLabel, { value: progress });
}


/***/ }),

/***/ "./lib/components/progress/LinearProgress.js":
/*!***************************************************!*\
  !*** ./lib/components/progress/LinearProgress.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ LinearBuffer)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_LinearProgress__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/LinearProgress */ "./node_modules/@mui/material/LinearProgress/LinearProgress.js");



function LinearBuffer({ setComplete }) {
    const [progress, setProgress] = react__WEBPACK_IMPORTED_MODULE_0__.useState(0);
    const [buffer, setBuffer] = react__WEBPACK_IMPORTED_MODULE_0__.useState(10);
    const progressRef = react__WEBPACK_IMPORTED_MODULE_0__.useRef(() => { });
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        progressRef.current = () => {
            if (progress === 100) {
                setComplete();
            }
            else {
                setProgress(progress + 1);
                if (buffer < 100 && progress % 5 === 0) {
                    const newBuffer = buffer + 1 + Math.random() * 10;
                    setBuffer(newBuffer > 100 ? 100 : newBuffer);
                }
            }
        };
    });
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        const timer = setInterval(() => {
            progressRef.current();
        }, 50);
        return () => {
            clearInterval(timer);
        };
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { width: '100%' } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_LinearProgress__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "buffer", value: progress, valueBuffer: buffer })));
}


/***/ }),

/***/ "./lib/components/table/CollapsibleTable.js":
/*!**************************************************!*\
  !*** ./lib/components/table/CollapsibleTable.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CollapsibleTable)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_Collapse__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material/Collapse */ "./node_modules/@mui/material/Collapse/Collapse.js");
/* harmony import */ var _mui_material_IconButton__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/IconButton */ "./node_modules/@mui/material/IconButton/IconButton.js");
/* harmony import */ var _mui_material_Table__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @mui/material/Table */ "./node_modules/@mui/material/Table/Table.js");
/* harmony import */ var _mui_material_TableBody__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @mui/material/TableBody */ "./node_modules/@mui/material/TableBody/TableBody.js");
/* harmony import */ var _mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/TableCell */ "./node_modules/@mui/material/TableCell/TableCell.js");
/* harmony import */ var _mui_material_TableContainer__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @mui/material/TableContainer */ "./node_modules/@mui/material/TableContainer/TableContainer.js");
/* harmony import */ var _mui_material_TableHead__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @mui/material/TableHead */ "./node_modules/@mui/material/TableHead/TableHead.js");
/* harmony import */ var _mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/TableRow */ "./node_modules/@mui/material/TableRow/TableRow.js");
/* harmony import */ var _mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Typography */ "./node_modules/@mui/material/Typography/Typography.js");
/* harmony import */ var _mui_material_Paper__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @mui/material/Paper */ "./node_modules/@mui/material/Paper/Paper.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_KeyboardArrowDown__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/icons-material/KeyboardArrowDown */ "./node_modules/@mui/icons-material/esm/KeyboardArrowDown.js");
/* harmony import */ var _mui_icons_material_KeyboardArrowUp__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/icons-material/KeyboardArrowUp */ "./node_modules/@mui/icons-material/esm/KeyboardArrowUp.js");

// import PropTypes from 'prop-types';














function createData(sci, time, availability) {
    const datacentres = Array.from({ length: 2 }, (_, index) => ({
        label: `Data Centre ${index + 1}`,
        details: {
            cpu: {
                usage: Number((Math.random() * 100).toFixed(2)),
                time: Math.floor(Math.random() * 10000),
                frequency: Number((Math.random() * 3 + 2).toFixed(2))
            },
            memory: {
                energy: Number((Math.random() * 1000).toFixed(2)),
                used: Math.floor(Math.random() * 1000000)
            },
            network: {
                io: Number((Math.random() * 100).toFixed(2)),
                connections: Math.floor(Math.random() * 50)
            }
        }
    }));
    return { sci, time, availability, datacentres };
}
function Row({ row, checkedIndex, setSelectedIndex, rowIndex }) {
    const [open, setOpen] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(false);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__["default"], null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: { display: 'flex', alignItems: 'center' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], null, rowIndex),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_IconButton__WEBPACK_IMPORTED_MODULE_5__["default"], { "aria-label": "expand row", size: "small", onClick: () => setOpen(!open) }, open ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_KeyboardArrowUp__WEBPACK_IMPORTED_MODULE_6__["default"], null) : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_KeyboardArrowDown__WEBPACK_IMPORTED_MODULE_7__["default"], null)),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Checkbox, { checked: checkedIndex, onClick: setSelectedIndex }))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null, row.sci),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "right" }, row.time),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "center" }, row.availability)),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__["default"], null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { style: { paddingBottom: 0, paddingTop: 0 }, colSpan: 4 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Collapse__WEBPACK_IMPORTED_MODULE_8__["default"], { in: open, timeout: "auto", unmountOnExit: true },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_9__["default"], { sx: { m: 1 } }, row.datacentres.map((datacentre, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_9__["default"], { key: index, sx: {
                            mb: 2,
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            p: 2
                        } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold', mb: 1 }, variant: "subtitle1" }, datacentre.label),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { container: true, spacing: 2, sx: { display: 'flex', justifyContent: 'space-between' } },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: {
                                    display: 'flex',
                                    flexDirection: 'column',
                                    flexGrow: 1
                                } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold' } }, "CPU"),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { style: { paddingInlineStart: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Usage: ",
                                        datacentre.details.cpu.usage,
                                        " %"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Time: ",
                                        datacentre.details.cpu.time,
                                        " \u03BCs"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Frequency: ",
                                        datacentre.details.cpu.frequency,
                                        " GHz"))),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: {
                                    display: 'flex',
                                    flexDirection: 'column',
                                    flexGrow: 1
                                } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold' } }, "Memory"),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { style: { paddingInlineStart: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Energy: ",
                                        datacentre.details.memory.energy,
                                        " \u03BCJ"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Used: ",
                                        datacentre.details.memory.used,
                                        " Bytes"))),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Grid2, { sx: {
                                    display: 'flex',
                                    flexDirection: 'column',
                                    flexGrow: 1
                                } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Typography__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { fontWeight: 'bold' } }, "Network"),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", { style: { paddingInlineStart: '10px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "IO: ",
                                        datacentre.details.network.io,
                                        " B/s"),
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                                        "Connections: ",
                                        datacentre.details.network.connections)))))))))))));
}
const rows = [
    createData(12.33, 4500, '++'),
    createData(14.12, 5200, '+'),
    createData(10.89, 4300, '+++')
];
function CollapsibleTable({ checkedIndex, setCheckedIndex }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableContainer__WEBPACK_IMPORTED_MODULE_10__["default"], { component: _mui_material_Paper__WEBPACK_IMPORTED_MODULE_11__["default"] },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Table__WEBPACK_IMPORTED_MODULE_12__["default"], { "aria-label": "collapsible table" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableHead__WEBPACK_IMPORTED_MODULE_13__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableRow__WEBPACK_IMPORTED_MODULE_2__["default"], null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], null, "SCI"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "right" }, "Est. Time (s)"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableCell__WEBPACK_IMPORTED_MODULE_3__["default"], { align: "center" }, "Availability"))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_TableBody__WEBPACK_IMPORTED_MODULE_14__["default"], null, rows.map((row, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Row, { key: index, row: row, rowIndex: index, checkedIndex: index === checkedIndex, setSelectedIndex: () => {
                    const newValue = index === checkedIndex ? null : index;
                    setCheckedIndex(newValue);
                } })))))));
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
/* harmony export */   MainWidget: () => (/* binding */ MainWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _components_VerticalLinearStepper__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/VerticalLinearStepper */ "./lib/components/VerticalLinearStepper.js");



// import BandHighLight from './components/BandHighLight';
// import ElementHighlights from './components/ElementHighlights';
// import MapComponent from './components/map/MapComponent';

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
function GridContent() {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Grid2, { sx: { width: '100%', px: 3, py: 5 } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_VerticalLinearStepper__WEBPACK_IMPORTED_MODULE_3__["default"], null)));
}
/**
 * React component for a counter.
 *
 * @returns The React component
 */
const App = () => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: styles.main },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Paper, { style: styles.grid },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(GridContent, null))));
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

/***/ "./node_modules/@mui/icons-material/esm/KeyboardArrowDown.js":
/*!*******************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/KeyboardArrowDown.js ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M7.41 8.59 12 13.17l4.59-4.58L18 10l-6 6-6-6z"
}), 'KeyboardArrowDown'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/KeyboardArrowUp.js":
/*!*****************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/KeyboardArrowUp.js ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M7.41 15.41 12 10.83l4.59 4.58L18 14l-6-6-6 6z"
}), 'KeyboardArrowUp'));

/***/ })

}]);
//# sourceMappingURL=lib_index_js.a27eafd0473584f47273.js.map