export type Mods = Record<string, string | boolean | undefined>;

export function classNames(
  cls: string,
  mods: Mods = {},
  additional: Array<string | undefined> = [],
): string {
  return [
    cls,
    ...additional.filter(Boolean),
    ...Object.entries(mods)
      .filter(([_, val]) => Boolean(val))
      .map(([className, _]) => className),
  ].join(" ");
}
