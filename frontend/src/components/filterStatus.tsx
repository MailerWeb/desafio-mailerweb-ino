import { Box, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import type { FilterStatusProps } from "../type/filter";

const FilterStatus = ({
    statusFilter,
    setStatusFilter,
    categories,
}: FilterStatusProps) => {
    return (
        <Box
            sx={{
                mb: 3,
                display: "flex",
                justifyContent: "flex-end",
            }}
        >
            <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Situação</InputLabel>
                <Select
                    value={statusFilter}
                    label="Situação"
                    onChange={setStatusFilter}
                >
                    <MenuItem value="all">Todas as tarefas</MenuItem>
                    <MenuItem value="pending">Pendentes</MenuItem>
                    <MenuItem value="completed">Concluídas</MenuItem>
                    {categories.map((category) => (
                        <MenuItem key={category.id} value={category.id}>
                            {category.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Box>
    );
};

export default FilterStatus;
