declare module "@mui/material/styles" {
  interface Theme {
    layout: {
      appbar: {
        height: number
      },
      footer: {
        height: number
      }
    };
  }

  interface ThemeOptions {
    layout: {
      appbar: {
        height: number
      },
      footer: {
        height: number
      }
    };
  }

  interface Palette {
    accent: {
      main: string;
    };
  }
  interface PaletteOptions {
    accent: {
      main: string;
    };
  }
}

export const commonThemeOptions = {
  typography: {
    fontFamily: [
      "Inter, sans-serif",
    ].join(','),
  },
  shape: {
    borderRadius: 20,
  },
  layout: {
    appbar: {
      height: 70,
    },
    footer: {
      height: 50
    }
  },
}