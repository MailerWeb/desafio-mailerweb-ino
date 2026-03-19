import { useState } from "react";
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
} from "@mui/material";
import type { CategoryFormProps } from "../type/task";

const CategoryForm = ({ open, onClose, onSave }: CategoryFormProps) => {
    const [name, setName] = useState("");

    const handleSave = () => {
        onSave(name);
        setName("");
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
            <DialogTitle>Nova Categoria</DialogTitle>
            <DialogContent sx={{ pt: 1 }}>
                <TextField
                    label="Nome da Categoria"
                    fullWidth
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    autoFocus
                    margin="dense"
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancelar</Button>
                <Button
                    onClick={handleSave}
                    variant="contained"
                    disabled={!name.trim()}
                >
                    Salvar
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default CategoryForm;
