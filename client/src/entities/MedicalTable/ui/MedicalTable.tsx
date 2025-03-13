import { DataGrid } from "@mui/x-data-grid";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import { classNames } from "@/shared/lib/classNames";
import cls from "./MedicalTable.module.scss";
import { Box } from "@mui/material";

interface MedicalTableProps {
  className?: string;
  columns: GridColDef[];
  rows: GridRowsProp;
  handleClick: (id: string) => void;
}

export const MedicalTable = (props: MedicalTableProps) => {
  const { columns, rows, className, handleClick } = props;
  return (
    <Box className={classNames(cls.MedicalTable, {}, [className])}>
      <DataGrid
        rows={rows}
        columns={columns}
        onRowDoubleClick={(params: any) => handleClick(params.id as string)}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 5,
            },
          },
        }}
        pageSizeOptions={[5]}
      />
    </Box>
  );
};
