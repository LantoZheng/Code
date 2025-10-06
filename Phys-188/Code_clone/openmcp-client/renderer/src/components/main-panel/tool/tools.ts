import type { ToolCallResponse } from '@/hook/type';
import type { Edge, Node, NodeDataView } from './auto-detector/diagram';

export interface ToolStorage {
    activeNames: any[];
    currentToolName: string;
    lastToolCallResponse?: ToolCallResponse | string;
    formData: Record<string, any>;
    autoDetectDiagram?: {
        edges?: Edge[];
        views?: NodeDataView[];
        [key: string]: any;
    }
}
