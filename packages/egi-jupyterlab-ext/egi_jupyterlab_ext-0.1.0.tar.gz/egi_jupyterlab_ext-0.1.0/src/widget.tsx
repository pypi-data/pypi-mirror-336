import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Grid2, Paper } from '@mui/material';
import RefreshButton from './components/RefreshButton';
import NumberInput from './components/NumberInput';

// import BandHighLight from './components/BandHighLight';
// import ElementHighlights from './components/ElementHighlights';
// import MapComponent from './components/map/MapComponent';
// import VerticalLinearStepper from './components/VerticalLinearStepper';

const styles: Record<string, React.CSSProperties> = {
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

export const DEFAULT_REFRESH_RATE = 2;

function debounce<T extends (...args: any[]) => void>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timer);
    timer = setTimeout(() => func(...args), delay);
  };
}

/**
 * React component for a counter.
 *
 * @returns The React component
 */
const App = (): JSX.Element => {
  const iframeRef = React.useRef<HTMLIFrameElement>(null);

  const [refreshRateS, setRefreshRateS] =
    React.useState<number>(DEFAULT_REFRESH_RATE);

  const [iframeSrc, setIframeSrc] = React.useState<string>(
    `http://localhost:3000/d-solo/ceetwcgabhgcgb/ping-go-server?orgId=1&from=1741098858351&to=1741100658351&timezone=browser&panelId=1&__feature.dashboardSceneSolo&refresh=${refreshRateS}s`
  );

  React.useEffect(() => {
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
  const debouncedSetRefreshRateS = React.useMemo(
    () => debounce((value: number) => setRefreshRateS(value), 1000),
    []
  );

  // Call the debounced function on number change
  function handleNumberChange(value: string) {
    const parsedValue = Number(value);
    if (!isNaN(parsedValue)) {
      debouncedSetRefreshRateS(parsedValue);
    }
  }

  return (
    <div style={styles.main}>
      <Paper style={styles.grid}>
        {/* <GridContent /> */}

        <iframe
          src={iframeSrc}
          width="450"
          height="200"
          frameBorder="0"
          sandbox="allow-scripts allow-same-origin"
          ref={iframeRef}
        ></iframe>
        <Grid2>
          <RefreshButton handleRefreshClick={handleRefreshClick} />
          <NumberInput
            // currentRefreshValue={refreshRateS}
            handleRefreshNumberChange={newValue => handleNumberChange(newValue)}
          />
        </Grid2>
      </Paper>
    </div>
  );
};

/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
export class MainWidget extends ReactWidget {
  /**
   * Constructs a new CounterWidget.
   */
  constructor() {
    super();
    this.addClass('jp-ReactWidget');
  }

  render(): JSX.Element {
    return <App />;
  }
}
