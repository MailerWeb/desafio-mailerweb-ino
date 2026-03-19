import type { Category } from "./task";

export interface FilterStatusProps {
  statusFilter: string | number;
  setStatusFilter: (e: any) => void;
  categories: Category[];
}

export interface FilterCategProps {
  open: boolean;
  onClose: (e: any) => void;
}
