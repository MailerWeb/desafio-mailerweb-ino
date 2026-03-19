export interface Task {
  id: number;
  title: string;
  description: string;
  is_completed: boolean;
  categories: number[];
}

export interface TasksListType {
  tasksList: Task[];
  categories: Category[];
  handleOpenEditForm: (value: Task) => void;
  handleDeleteTask: (value: Task) => void;
  handleCompleteTask: (value: Task) => void;
  handleShareWith: (value: number) => void;
}
export interface TaskFormProps {
  open: boolean;
  onClose: () => void;
  onSave: (task: Partial<Task>) => void;
  categories: Category[];
  taskToEdit?: Task | null;
}

export interface Category {
  id: number;
  name: string;
  color?: string;
}

export interface CategoryFormProps {
  open: boolean;
  onClose: () => void;
  onSave: (name: string) => void;
}
