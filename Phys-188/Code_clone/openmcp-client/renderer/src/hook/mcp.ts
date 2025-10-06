import { reactive } from "vue";

interface TypeAble {
    type: string;
}

export function getDefaultValue(property: TypeAble): any {    
    if (property.type === 'number' || property.type === 'integer') {
        return 0;
    } else if (property.type === 'boolean') {
        return false;
    } else if (property.type === 'object') {
        return {};
    } else if (property.type === 'array') {
        return [];
    } else {
        return '';
    }
}

export function normaliseJavascriptType(type: string) {
    switch (type) {
        case 'integer':
            return 'number';
        case 'number':
            return 'number';
        case 'boolean':
            return 'boolean';
        case 'string':
            return 'string';
        case 'array':
            return 'array';
        default:
            return type;
    }
}

export const mcpSetting = reactive({
    language: 'zh',
    timeout: 60,
    proxyServer: '',
});