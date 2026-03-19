import {
    Box,
    Paper,
    List,
    ListItem,
    ListItemText,
    IconButton,
    Checkbox,
    Typography,
    Chip,
    Stack,
} from "@mui/material";
import Edit from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import type { TasksListType } from "../type/task";
import { Share } from "@mui/icons-material";

const TasksList = ({
    tasksList,
    categories,
    handleOpenEditForm,
    handleDeleteTask,
    handleCompleteTask,
    handleShareWith,
}: TasksListType) => {
    return (
        <Paper elevation={2} sx={{ borderRadius: 2, overflow: "hidden" }}>
            <List sx={{ p: 0 }}>
                {tasksList.length === 0 ? (
                    <ListItem>
                        <ListItemText
                            primary="Nenhuma tarefa encontrada."
                            sx={{
                                textAlign: "center",
                                py: 3,
                                color: "text.secondary",
                            }}
                        />
                    </ListItem>
                ) : (
                    tasksList.map((task) => (
                        <ListItem
                            key={task.id}
                            secondaryAction={
                                <Box>
                                    <IconButton
                                        edge="end"
                                        aria-label="edit"
                                        onClick={() => handleShareWith(task.id)}
                                        sx={{ mr: 1 }}
                                    >
                                        <Share />
                                    </IconButton>
                                    <IconButton
                                        edge="end"
                                        aria-label="edit"
                                        onClick={() => handleOpenEditForm(task)}
                                        sx={{ mr: 1 }}
                                    >
                                        <Edit />
                                    </IconButton>
                                    <IconButton
                                        edge="end"
                                        aria-label="delete"
                                        color="error"
                                        onClick={() => handleDeleteTask(task)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </Box>
                            }
                            divider
                        >
                            <Checkbox
                                checked={task.is_completed}
                                onChange={() => handleCompleteTask(task)}
                                color="primary"
                            />
                            <ListItemText
                                primary={task.title}
                                secondary={
                                    <Box component="span">
                                        <Typography
                                            variant="body2"
                                            component="span"
                                            display="block"
                                        >
                                            {task.description}
                                        </Typography>
                                        <Stack
                                            direction="row"
                                            spacing={1}
                                            sx={{ mt: 1 }}
                                        >
                                            {task.categories?.map((catId) => {
                                                const cat = categories.find(
                                                    (c) => c.id === catId,
                                                );
                                                return cat ? (
                                                    <Chip
                                                        key={catId}
                                                        label={cat.name}
                                                        size="small"
                                                        variant="outlined"
                                                    />
                                                ) : null;
                                            })}
                                        </Stack>
                                    </Box>
                                }
                            />
                        </ListItem>
                    ))
                )}
            </List>
        </Paper>
    );
};

export default TasksList;
