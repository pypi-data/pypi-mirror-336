#!/usr/bin/env python3

import argparse
import os
import yaml
import sys
import re

def convert_docker_to_singularity(docker_compose_path, output_path=None):
    """
    Convert a docker-compose.yml file to a singularity-compose.yml file.
    
    Args:
        docker_compose_path: Path to the docker-compose.yml file
        output_path: Path to write the singularity-compose.yml file (default: singularity-compose.yml)
    """
    if output_path is None:
        output_path = "singularity-compose.yml"
    
    # Read the docker-compose.yml file
    try:
        with open(docker_compose_path, 'r') as f:
            docker_compose = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading docker-compose file: {e}")
        return False
    
    # Initialize singularity-compose structure
    singularity_compose = {
        'version': '1.0',
        'instances': {}
    }
    
    # Check if docker-compose version is supported
    if 'version' in docker_compose:
        print(f"Converting from docker-compose version: {docker_compose['version']}")
    
    # Convert services to instances
    if 'services' not in docker_compose or not docker_compose['services']:
        print("No services found in docker-compose file")
        return False
    
    for service_name, service_config in docker_compose['services'].items():
        instance = {}
        
        # Convert image
        if 'image' in service_config:
            instance['container'] = f"docker://{service_config['image']}"
        elif 'build' in service_config:
            # For build, we need to note that this requires manual intervention
            build_context = service_config['build']
            if isinstance(build_context, dict):
                build_context = build_context.get('context', '.')
            instance['container'] = f"# TODO: Build from {build_context} and specify path to .sif file"
            print(f"Warning: Service {service_name} uses 'build'. You'll need to manually build a Singularity image.")
        else:
            print(f"Warning: No image or build specified for {service_name}")
            continue
        
        # Convert volumes
        if 'volumes' in service_config:
            instance['volumes'] = []
            for volume in service_config['volumes']:
                if isinstance(volume, str):
                    # Parse volume string (host:container[:mode])
                    parts = volume.split(':')
                    if len(parts) >= 2:
                        host_path = parts[0]
                        container_path = parts[1]
                        # Preserve mount options if present
                        if len(parts) > 2:
                            instance['volumes'].append(f"{host_path}:{container_path}:{parts[2]}")
                        else:
                            instance['volumes'].append(f"{host_path}:{container_path}")
                    else:
                        print(f"Warning: Unsupported volume format: {volume}")
                elif isinstance(volume, dict):
                    # Handle volume with explicit source, target, etc.
                    if 'source' in volume and 'target' in volume:
                        mount_str = f"{volume['source']}:{volume['target']}"
                        if 'read_only' in volume and volume['read_only']:
                            mount_str += ":ro"
                        instance['volumes'].append(mount_str)
                    else:
                        print(f"Warning: Unsupported volume format: {volume}")
        
        # Convert environment variables
        if 'environment' in service_config:
            instance['environment'] = {}
            env_vars = service_config['environment']
            if isinstance(env_vars, dict):
                instance['environment'] = env_vars
            elif isinstance(env_vars, list):
                for env_var in env_vars:
                    if '=' in env_var:
                        key, value = env_var.split('=', 1)
                        instance['environment'][key] = value
                    else:
                        print(f"Warning: Unsupported environment format: {env_var}")
        
        # Convert ports
        if 'ports' in service_config:
            instance['ports'] = []
            for port in service_config['ports']:
                if isinstance(port, str):
                    # Parse port string (host:container)
                    parts = port.split(':')
                    if len(parts) >= 2:
                        host_port = parts[0]
                        container_port = parts[1]
                        instance['ports'].append(f"{host_port}:{container_port}")
                    else:
                        instance['ports'].append(f"{port}:{port}")
                elif isinstance(port, dict):
                    # Handle port with explicit published, target, etc.
                    if 'published' in port and 'target' in port:
                        instance['ports'].append(f"{port['published']}:{port['target']}")
                    else:
                        print(f"Warning: Unsupported port format: {port}")
        
        # Convert command
        if 'command' in service_config:
            command = service_config['command']
            if isinstance(command, list):
                instance['command'] = ' '.join(command)
            else:
                instance['command'] = command
        
        # Convert working_dir
        if 'working_dir' in service_config:
            instance['workdir'] = service_config['working_dir']
        
        # Convert restart policy
        if 'restart' in service_config:
            # Singularity doesn't have direct restart policy equivalent
            print(f"Warning: Restart policy '{service_config['restart']}' for {service_name} not supported in Singularity")
        
        # Convert depends_on
        if 'depends_on' in service_config:
            instance['startorder'] = len(service_config['depends_on'])
            print(f"Warning: 'depends_on' for {service_name} converted to 'startorder', may need manual adjustment")
        
        # Add the instance to the singularity-compose file
        singularity_compose['instances'][service_name] = instance
    
    # Convert networks (limited support)
    if 'networks' in docker_compose:
        print("Warning: Singularity networking differs from Docker. Network configurations need manual review.")
    
    # Convert volumes (limited support)
    if 'volumes' in docker_compose and isinstance(docker_compose['volumes'], dict):
        print("Warning: Named volumes need to be manually configured in Singularity.")
    
    # Write the singularity-compose.yml file
    try:
        with open(output_path, 'w') as f:
            yaml.dump(singularity_compose, f, default_flow_style=False)
        print(f"Successfully converted to {output_path}")
        print("Note: Please review the generated file as some features may require manual adjustment.")
        return True
    except Exception as e:
        print(f"Error writing singularity-compose file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert docker-compose.yml to singularity-compose.yml')
    parser.add_argument('input', help='Path to docker-compose.yml file')
    parser.add_argument('-o', '--output', help='Path to output singularity-compose.yml file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} does not exist")
        sys.exit(1)
    
    success = convert_docker_to_singularity(args.input, args.output)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
