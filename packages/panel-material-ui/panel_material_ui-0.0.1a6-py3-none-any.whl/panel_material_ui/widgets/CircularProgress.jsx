import CircularProgress from "@mui/material/CircularProgress";

export function render({model}) {
  const [value] = model.useState("value");
  const [variant] = model.useState("variant");
  const [color] = model.useState("color");
  const [sx] = model.useState("sx");

  return (
    <CircularProgress variant={variant} color={color} value={value} sx={sx} />
  );
}
