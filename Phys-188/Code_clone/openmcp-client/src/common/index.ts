import { CommandHandlerDescriptor, IRegisterCommandItem, IRegisterTreeDataProviderItem, TreeDataProviderConstructor } from "./index.dto.js";

export const registerCommands = new Array<[string, IRegisterCommandItem]>();
export const registerTreeDataProviders = new Map<string, IRegisterTreeDataProviderItem<any>>();

export function RegisterCommand(command: string, options?: any) {
    return function (target: any, propertyKey: string, descriptor: CommandHandlerDescriptor) {
        const handler = descriptor.value;        
        
        if (handler) {
            registerCommands.push([command, { handler, target, propertyKey, options }]);
        }

        return descriptor;
    }
}

export function RegisterTreeDataProvider<T>(providerId: string, options?: any) {
    return function (target: TreeDataProviderConstructor<T>) {

        target.prototype.__openmcp_namespace = providerId;
        
        registerTreeDataProviders.set(providerId, {
            providerConstructor: target,
            options
        });
    }
}