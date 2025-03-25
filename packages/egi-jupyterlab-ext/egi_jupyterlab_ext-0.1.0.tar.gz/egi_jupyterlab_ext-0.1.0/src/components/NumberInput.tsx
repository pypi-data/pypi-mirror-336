import { TextField } from '@mui/material';
import React from 'react';
import { DEFAULT_REFRESH_RATE } from '../widget';

interface INumberInput {
  // currentRefreshValue: number;
  handleRefreshNumberChange: (newValue: string) => void;
}

export default function NumberInput({
  // currentRefreshValue,
  handleRefreshNumberChange
}: INumberInput) {
  return (
    <TextField
      id="outlined-number"ho
      label="Refresh(S)"
      type="number"
      slotProps={{
        inputLabel: {
          shrink: true
        }
      }}
      onChange={event => handleRefreshNumberChange(event.target.value)}
      // value={currentRefreshValue}
      defaultValue={DEFAULT_REFRESH_RATE}
      size="small"
      sx={{ maxWidth: 90 }}
    />
  );
}
